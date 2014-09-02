Pychievements: The Python Achievments Framework!
================================================

|build| |docs| |coverage| |downloads| |license|

.. |coverage| image:: https://coveralls.io/repos/PacketPerception/pychievements/badge.png?branch=master
    :target: https://coveralls.io/r/PacketPerception/pychievements?branch=master

.. |build| image:: https://travis-ci.org/PacketPerception/pychievements.svg?branch=master
    :target: https://travis-ci.org/PacketPerception/pychievements

.. |docs| image:: https://readthedocs.org/projects/pychievements/badge/?version=latest
    :target: http://pychievements.readthedocs.org/en/latest/

.. |downloads| image:: https://pypip.in/download/pychievements/badge.svg
    :target: https://pypi.python.org/pypi/pychievements/
    :alt: Downloads

.. |license| image:: https://pypip.in/license/pychievements/badge.svg
    :target: https://pypi.python.org/pypi/pychievements/
    :alt: License

**Pychievements** is a framework for creating and tracking achievements within a Python application.
It includes functions specifically for creating command line applications, though it is flexible 
enough to be used for any application such as web applications.

See the examples_ to get a good feel for what Pychievements offers. Documentation can be found RTD:
http://pychievements.readthedocs.org/en/latest/

.. _examples: https://github.com/PacketPerception/pychievements/tree/master/examples


Features:
---------
 - Create Achievements with any number of "goals" (based on levels) that can be reached
 - Flexible design makes it easy to customize the way levels are tracked
 - Easy to add new achievements later
 - Pluggable backend for storing tracked information in different formats to different locations
 - Achievements can be filtered by category or keywords
 - Easily specify "Icons" for individual goals within an achievement for dual states (achieved and
   unachieved)


Example
-------

A simple achievement. ::

    class MyAchievement(Achievement):
        name = "My Achievement"
        category = "achievements"
        keywords = ("my", "achievement")
        goals = (
            {"level": 10, "name": "Level 1", "icon": icons.star, "description": "Level One"},
            {"level": 20, "name": "Level 2", "icon": icons.star, "description": "Level Two"},
            {"level": 30, "name": "Level 3", "icon": icons.star, "description": "Level Three"},
        )


Increment a level for a user. ::

    tracker.increment(user_id, MyAchievment)


Re-evaluating a level for a user based on arguments (requires the evaluate function to be defined 
or the Achievement). ::

    tracker.evaluate(user_id, MyAchievement, some, extra, args)


Retrieve achievements. ::

    tracker.achievements()                # retrieves all registered achievements in the tracker
    tracker.achieved(uid, achievement)    # all achieved goals by uid for achievement
    tracker.unachieved(uid, achievement)  # all unachieved goals by uid for achievement
    tracker.current(uid, achievement)     # goal currently being worked torwards by uid


Installation
------------

To install pychievements, simply: ::

    $ pip install pychievements


License
-------

Pychievements is licensed under the MIT License, see the LICENSE_.

.. _LICENSE: http://github.com/PacketPerception/pychievements/blob/master/LICENSE


Contribute
----------

If you'd like to contribute, simply fork `the repository`_, commit your changes
to the **master** branch (or branch off of it), and send a pull request. Make
sure you add yourself to AUTHORS_.


.. _`the repository`: http://github.com/PacketPerception/pychievements
.. _AUTHORS: http://github.com/PacketPerception/pychievements/blob/master/AUTHORS


Roadmap
-------
- More backends
- More icons
