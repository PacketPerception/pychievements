.. _getting-started:

Getting Started
===============

*Getting Started* will guide you through creating your first achievements an introducing you to
the pieces of the system. From there, visit the :doc:`reference` for in-depth information.

Installing Pychievements
------------------------

Pychievements can be installed with ``pip``:
 ::

    $ pip install pychievements

.. note:
    There are no required dependencies for pychievements. If you would like to the ``cli`` tools,
    then then you will have to install the *clint* library. You can use pip to install the 
    optional ``cli`` dependencies like so: ``pip install pychievements[cli]``


Introduction to Pychievments
----------------------------

Pychievements has a number of modules that you'll need to be at least familiar with:

    tracker
        The default achievement tracker for pychievements is instantiated at import and is used to
        track all registered achievements for specific *tracked_ids*.

    Achievement
        Base Achievment class.

    icons.Icon
        Base Icon class. Icons are used to know what to display for a given goal within an
        achievement and have two states, achieved and unachieved.

    backends.AchievementBackend
        Pychievements have pluggable backends for storing tracked achievement data. The default
        ``AchievementBackend`` simply keeps everyting in memory, meaning it will be lost when the
        application is closed. The backend the tracker is using can be updated with the
        ``set_backend`` method. 

    signals
        You can register functions as callbacks that can *recieve* Pychievement signals. Signals can
        be generated when a level is changed, when a new goal is reached, or when all goals have
        been achieved for a given achievement.


Achievements
^^^^^^^^^^^^

At the core of Pychievements is the ``Achievement`` class. It is used to define goals that are
obtained at specified *levels*. Levels are simply an integer. At a minimum, achievements must have
the following attributes defined:

* name : Display name of your achievement
* category : Defaults to "achievements"
* goals : A tuple of *goals*. A *goal* is a dictionary with the following keys: *["level", "name",
  "icon", "description"]*

An example Achievement class: ::

    class MyAchievement(Achievement):
        name = "My Achievement"
        category = "achievements"
        keywords = ("my", "achievement")
        goals = (
            {"level": 10, "name": "Level 1", "icon": icons.star, "description": "Level One" },
            {"level": 20, "name": "Level 2", "icon": icons.star, "description": "Level Two" },
            {"level": 30, "name": "Level 3", "icon": icons.star, "description": "Level Three" },
        )

An achievements current level for an id can tracked with either the ``increment`` or ``evaluate``
functions, which the achievment can override to provide custom level manipulation.


The Tracker
^^^^^^^^^^^

A singleton ``tracker`` is created on import that is available as ``pychievements.tracker``. The
tracker provides an interface for interacting with registered achievements for a given
``tracked_id``. The tracker lets you:

* increment level of an achievement for a tracked_id
* evaluate level of an achievement for a tracked_id
* query all achievements by category or keywords
* query all achieved goals of an achievement for a tracked_id
* query all unachieved goals of an achievement for a tracked_id
* query the current goal being worked towards of an achievement for a tracked_id

The tracker works with the configured backend to store and retrieve all of the tracked levels.


Icons
^^^^^

Icons are simple classes that provide the "icon" (or what is displayed) for an achievment goal. It
must define what to display for when the goal has been achieved (``achieved``) or not
(``unachieved``)


Examples
--------

The easiest way to get started to check out the examples in the `examples`_ folder in the
`the repository`_. Then check out the :doc:`reference` for more information.

.. _examples: https://github.com/PacketPerception/pychievements/tree/master/examples
.. _`the repository`: https://github.com/PacketPerception/pychievements
