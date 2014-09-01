class AchievementBackend(object):
    """
    AchievementBackend

    Achievement backends implement the getting/setting/updating of achievements for ``tracked_id``.
    Achievements in the system are tracked for a specific, unique ID, ``tracked_id``.

    AchievementBackend is the most basic implementation of an AchievementBackend, storing all
    tracked information in memory and never persisting it. All of the functions of an
    AchievementBackend work to retrieve an ``Achievemnet`` instance for a given ``tracked_id``, and
    run the appropriate function on it, storing the results. In the least, storing results for a
    sepcific achievemnt, for a specific ``target_id`` should include the ``target_id``, the
    ``Achievement`` class name (``Achievement.__name__``), and the current level
    (``Achievement.current``)
    """
    def __init__(self):
        self._tracked = {}

    def achievement_for_id(self, tracked_id, achievement):
        """ Retrieves the current ``Achievement`` for the given ``tracked_id``. If the given
        ``tracked_id`` does not exist yet, it should be created. Also, if the given ``tracked_id``
        hasn't tracked the given ``Achievement`` yet, a new instance of the ``Achievement`` should
        be created for the given ``tracked_id``"""
        if tracked_id not in self._tracked:
            self._tracked[tracked_id] = {}
        if achievement.__name__ not in self._tracked[tracked_id]:
            self._tracked[tracked_id][achievement.__name__] = achievement()
        return self._tracked[tracked_id][achievement.__name__]

    def set_level_for_id(self, tracked_id, achievement, level):
        """ Set the ``level`` for an ``Achievement`` for the given ``trakced_id`` """
        if tracked_id not in self._tracked:
            self._tracked[tracked_id] = {}
        if achievement.__name__ not in self._tracked[tracked_id]:
            self._tracked[tracked_id][achievement.__name__] = achievement(current=level)
        self._tracked[tracked_id][achievement.__name__].set_level(level)
