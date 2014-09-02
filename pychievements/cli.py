from . import tracker as _defaulttracker
from .achievements import Achievement
from inspect import isclass as _isclass

try:
    from itertools import zip_longest as _zip_longest
except ImportError:
    from itertools import izip_longest as _zip_longest


def print_goal(goal, achieved=False, level=None, indent=2):
    """ Print a goals description with its icon. Achieved (True/False) will choose the correct icon
    from the goal. If a level is specified, a tracker line will be added under the icon showing
    the current level out of the required level for the goal. If level is > the required level,
    achieved will be set to true.
    """
    from clint.textui import puts
    from clint.textui import indent as _indent
    from clint.textui.cols import columns, console_width
    if level is not None and level >= goal['level']:
        achieved = True
    icon = (goal['icon'].achieved() if achieved else goal['icon'].unachieved()).split('\n')
    maxiw = max([len(str(_)) for _ in icon])
    descw = console_width({})-maxiw-(indent + 4)
    desc = '{0}\n{1}\n\n{2}'.format(goal['name'], '-'*len(goal['name']),
                                    columns([goal['description'], descw])).split('\n')
    if level is not None:
        if level > goal['level']:
            level = goal['level']
        maxitw = max([len(_) for _ in icon])
        icon.append(("%d/%d" % (level, goal['level'])).center(maxitw))
    with _indent(indent):
        for i, d in _zip_longest(icon, desc):
            puts("{1:{0}}    {2}".format(maxiw, str(i) if i is not None else "",
                                         d.strip() if d is not None else ""))


def print_goals(achievement_or_iter, indent=2):
    """
    Displays all of the available goals registered for the given achievement(s)
    """
    from clint.textui import puts
    from clint.textui.cols import console_width
    from clint.textui import indent as _indent
    if _isclass(achievement_or_iter) and issubclass(achievement_or_iter, Achievement):
        achievement_or_iter = [achievement_or_iter]

    for achievement in achievement_or_iter:
        with _indent(indent):
            puts("{0}\n{1}\n".format(achievement.name, '='*(console_width({})-indent-2)))
        for goal in achievement.goals:
            print_goal(goal, True, indent=indent)
            puts("\n")


def print_goals_for_tracked(tracked_id, achievement_or_iter=None, achieved=True, unachieved=False,
                            only_current=False, level=False, category=None, keywords=[],
                            indent=2, tracker=None):
    """
    Prints goals for a specific ``tracked_id`` from as tracked by a ``tracker``. By default, this
    will print out all achieved goals for every achievement in the ``tracker``.

    Arguments:

        achievment_or_iter
            If ``None``, this will print goals for all achievements registered with the ``tracker``.
            Otherwise an ``Achievement`` or list of achievements can be given to show goals for.

        achieved
            If True, prints out goals that have allready been achieved.

        unachieved
            If True, prints out goals that have not been achieved.

        only_current
            If True, only prints the goal currently being worked on (next to be achieved). This will
            override the ``achieved`` and ``unachieved`` options.

        category
            Category to filter achievements from the tracker.

        keywords
            Keywords to filter achievements from the tracker.

        level
            If True, show the current level with the achievements

        tracker
            The tracker to use for getting information about achievements and ``tracked_id``. If
            ``tracker`` is ``None``, this will default to using the default tracker.
    """
    from clint.textui import puts
    from clint.textui import indent as _indent
    from clint.textui.cols import console_width
    if tracker is None:
        tracker = _defaulttracker

    if achievement_or_iter is None:
        achievement_or_iter = tracker.achievements()
    elif _isclass(achievement_or_iter) and issubclass(achievement_or_iter, Achievement):
        achievement_or_iter = [achievement_or_iter]

    for achievement in achievement_or_iter:
        with _indent(indent):
            puts("{0}\n{1}\n".format(achievement.name, '='*(console_width({})-indent-2)))
        current = tracker.current(tracked_id, achievement)
        cl = None if not level else current[0]
        if only_current:
            print_goal(current[1], level=current[0], indent=indent)
        else:
            goals = tracker.achieved(tracked_id, achievement) if achieved else []
            goals += tracker.unachieved(tracked_id, achievement) if unachieved else []
            for goal in goals:
                print_goal(goal, current[0] >= goal['level'], level=cl, indent=indent)
                puts("\n")
