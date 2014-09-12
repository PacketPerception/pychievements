class Achievement(object):
    """
    Base Achievement class.

    An achievement primarily consists of 'goals', being levels that can be reached. Instances of
    Achievements are used to track progress, and the current level for individual IDs. For this,
    an Achievement implements a number of functions to interact with the current level.
    Achievements can also have a ``category`` (string) and ``keywords`` (tuple of strings) that can
    be used to filter Achievements.

    Goals are defined as a tuple of tuples with the format:

    .. code-block:: python

        goals = (
            {'level': 10, 'name': 'Level 1', 'icon': icons.star, 'description': 'Level One'},
            {'level': 20, 'name': 'Level 2', 'icon': icons.star, 'description': 'Level Two'},
            {'level': 30, 'name': 'Level 3', 'icon': icons.star, 'description': 'Level Three'},
        )


    Arguments:

        level
            A positive integer that must be reached (greater than or equal) to be considered 'met'

        name
            A short name for the level

        icon
            The ``Icon`` to represent the level before it has been achieved. This must be an
            :py:mod:`pychievements.icons.Icon` class.

        .. note::
            There are simple ASCII icons available from :py:mod:`pychievements.icons`

        description
            A longer description of the level.



    Achievements can be updated in two ways: ``increment`` and ``evaluate``. Increment increments
    the current level given an optional set of arguments, where evaluate performs a custom
    evaluation a sets the current level based on that evaluation.

    Increment is best used when the application is aware of achievement tracking, and calls
    to increment can be placed throughout the application.

    Evaluate is best used when actions may happen externally, and cannot be tracked using repeated
    calls to increment. Evaluate will also return the list of achieved goals after it has performed
    its evaluation.

    An Achievement can be initialized with a ``current`` level, for example when restoring for a
    saved state.
    """
    name = 'Achievement'
    category = 'achievements'
    keywords = tuple()
    goals = tuple()

    def __init__(self, current=0):
        self._current = current
        self.goals = sorted(self.goals, key=lambda g: g['level'])  # make sure our goals are sorted

    def __repr__(self):
        return '<{0} category:\'{1}\' keywords:{2} {3}>'.format(self.name, self.category,
                                                                self.keywords, self._current)

    @property
    def current(self):
        """
        Returns the current level being achieved (meaning haven't achieved yet) as a tuple:

        ::
            (current_level, (required_level, name, icon, description))

        If all achievements have been achieved, the current level is returned with a None:

        ::
            (current_level, None)
        """
        g = [_ for _ in self.goals if self._current < _['level']]
        if g:
            return (self._current, g[0])
        return (self._current, None)

    @property
    def achieved(self):
        """
        Returns a list of achieved goals
        """
        return [_ for _ in self.goals if self._current >= _['level']]

    @property
    def unachieved(self):
        """
        Returns a list of goals that have not been met yet
        """
        return [_ for _ in self.goals if self._current < _['level']]

    def increment(self, amount=1, *args, **kwargs):
        """
        Increases the current level. Achievements can redefine this function to take options to
        increase the level based on given arguments. By default, this will simply increment the
        current count by ``amount`` (which defaults to 1).
        """
        self._current = self._current + amount

    def evaluate(self, *args, **kwargs):
        """
        Performs a custom evaluation to set the current level of an achievement. Returns a list of
        achieved goals after the level is determined.
        """
        return self.achieved

    def set_level(self, level):
        """
        Overrides the current level with the given level
        """
        self._current = level
