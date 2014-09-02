from .achievements import Achievement
from .backends import AchievementBackend
from .signals import goal_achieved, level_increased, highest_level_achieved
from inspect import isclass as _isclass


class AlreadyRegistered(Exception):
        pass


class NotRegistered(Exception):
    pass


class AchievementTracker(object):
    """
    AchievementTracker tracks achievements and current levels for ``tracked_id`` using a configured
    achievement backend.

    A default instance of Achievement tracker is created as a singleton when pycheivements is
    imported as ``pychievements.tracker``. Most often, this is what you will want to use.

    Arguments:

        backend:
            The backend to use for storing/retrieving achievement data. If ``None``, the default
            :py:class:`AchievementBackend` will be used, which stores all data in memory.

    .. note::
        The backend the tracker is using can be updated at any time using the :py:func:`set_backend`
        function.
    """
    def __init__(self, backend=None):
        self._registry = []
        self._backend = AchievementBackend() if backend is None else backend

    def set_backend(self, backend):
        """
        Configures a new backend for storing achievement data.
        """
        if not isinstance(backend, AchievementBackend):
            raise ValueError('Backend must be an instance of an AchievementBackend')
        self._backend = backend

    def register(self, achievement_or_iterable, **options):
        """
        Registers the given achievement(s) to be tracked.
        """
        if _isclass(achievement_or_iterable) and issubclass(achievement_or_iterable, Achievement):
            achievement_or_iterable = [achievement_or_iterable]
        for achievement in achievement_or_iterable:
            if not achievement.category:
                raise ValueError('Achievements must specify a category, could not register '
                                 '%s' % achievement.__name__)
            if achievement in self._registry:
                raise AlreadyRegistered('The achievement %s is already '
                                        'registered' % achievement.__name__)
            if achievement is not Achievement:
                self._registry.append(achievement)

    def unregister(self, achievement_or_iterable):
        """
        Un-registers the given achievement(s).

        If an achievement isn't already registered, this will raise NotRegistered.
        """
        if _isclass(achievement_or_iterable) and issubclass(achievement_or_iterable, Achievement):
            achievement_or_iterable = [achievement_or_iterable]
        for achievement in achievement_or_iterable:
            if achievement not in self._registry:
                raise NotRegistered('The achievement %s is not registered' % achievement.__name__)
            self._registry.remove(achievement)

    def is_registered(self, achievement):
        """
        Check if an achievement is registered with this `AchievementTracker`
        """
        return achievement in self._registry

    def achievements(self, category=None, keywords=[]):
        """
        Returns all registered achievements.

        Arguments:

            category
                Filters returned achievements by category. This is a strict string match.

            keywords
                Filters returned achievements by keywords. Returned achievements will match all
                given keywords
        """
        achievements = []
        for achievement in self._registry:
            if category is None or achievement.category == category:
                if not keywords or all([_ in achievement.keywords for _ in keywords]):
                    achievements.append(achievement)
        return achievements

    def achievement_for_id(self, tracked_id, achievement):
        """
        Returns ``Achievement`` for a given ``tracked_id``. Achievement can be an ``Achievement``
        class or a string of the name of an achievement class that has been registered with this
        tracker.

        Raises NotRegistered if the given achievement is not registered with the tracker.

        If ``tracked_id`` has not been tracked yet by this tracker, it will be created.
        """
        if isinstance(achievement, Achievement):
            achievement = achievement.__class__.__name__
        elif _isclass(achievement) and issubclass(achievement, Achievement):
            achievement = achievement.__name__

        a = [_ for _ in self._registry if _.__name__ == achievement]
        if a:
            return self._backend.achievement_for_id(tracked_id, a[0])
        raise NotRegistered('The achievement %s is not registered with this tracker' % achievement)

    def achievements_for_id(self, tracked_id, category=None, keywords=[]):
        """ Returns all of the achievements for tracked_id that match the given category and
        keywords """
        return self._backend.achievements_for_id(tracked_id, self.achievements(category, keywords))

    def _check_signals(self, tracked_id, achievement, old_level, old_achieved):
        cur_level = achievement.current[0]
        if old_level < cur_level:
            level_increased.send_robust(self, tracked_id=tracked_id, achievement=achievement)
        if old_achieved != achievement.achieved:
            new_goals = [_ for _ in achievement.achieved if _ not in old_achieved]
            goal_achieved.send_robust(self, tracked_id=tracked_id, achievement=achievement,
                                      goals=new_goals)
            if not achievement.unachieved:
                highest_level_achieved.send_robust(self, tracked_id=tracked_id,
                                                   achievement=achievement)
            return new_goals
        return False

    def increment(self, tracked_id, achievement, *args, **kwargs):
        """
        Increments an achievement for a given ``tracked_id``. Achievement can be an ``Achievement``
        class or a string of the name of an achievement class that has been registered with this
        tracker.

        Raises NotRegistered if the given achievement is not registered with the tracker.

        If ``tracked_id`` has not been tracked yet by this tracker, it will be created before
        incrementing.

        Returns an list of achieved goals if a new goal was reached, or False
        """
        achievement = self.achievement_for_id(tracked_id, achievement)
        cur_level = achievement.current[0]
        achieved = achievement.achieved[:]
        achievement.increment(*args, **kwargs)
        self._backend.set_level_for_id(tracked_id, achievement.__class__, achievement.current[0])
        return self._check_signals(tracked_id, achievement, cur_level, achieved)

    def evaluate(self, tracked_id, achievement, *args, **kwargs):
        """
        Evaluates an achievement for a given ``tracked_id``. Achievement can be an ``Achievement``
        class or a string of the name of an achievement class that has been registered with
        this tracker.

        Raises NotRegistered if the given achievement is not registered with the tracker.

        If ``tracked_id`` has not been tracked yet by this tracker, it will be created before
        evaluating.

        Returns list of achieved goals for the given achievement after evaluation
        """
        achievement = self.achievement_for_id(tracked_id, achievement)
        cur_level = achievement.current[0]
        achieved = achievement.achieved[:]
        result = achievement.evaluate(*args, **kwargs)
        self._backend.set_level_for_id(tracked_id, achievement.__class__, achievement.current[0])
        self._check_signals(tracked_id, achievement, cur_level, achieved)
        return result

    def current(self, tracked_id, achievement):
        """
        Returns ``current`` for a given tracked_id. See :ref:``Achievement``
        """
        achievement = self.achievement_for_id(tracked_id, achievement)
        return achievement.current

    def achieved(self, tracked_id, achievement):
        """
        Returns ``achieved`` for a given tracked_id. See :ref:``Achievement``
        """
        achievement = self.achievement_for_id(tracked_id, achievement)
        return achievement.achieved

    def unachieved(self, tracked_id, achievement):
        """
        Returns ``unachieved`` for a given tracked_id. See :ref:``Achievement``
        """
        achievement = self.achievement_for_id(tracked_id, achievement)
        return achievement.unachieved

    def set_level(self, tracked_id, achievement, level):
        """
        Returns ``set_level`` for a given tracked_id. See :ref:``Achievement``
        """
        achievement = self.achievement_for_id(tracked_id, achievement)
        cur_level = achievement.current[0]
        achieved = achievement.achieved[:]
        achievement.set_level(level)
        self._backend.set_level_for_id(tracked_id, achievement.__class__, achievement.current[0])
        self._check_signals(tracked_id, achievement, cur_level, achieved)

    def get_tracked_ids(self):
        """ Returns all tracked ids """
        return self._backend.get_tracked_ids()

    def remove_id(self, tracked_id):
        """ Remove all tracked information for tracked_id """
        self._backend.remove_id(tracked_id)
