Pychievements: The Python Achievments Framework!
================================================

|docs|

**Pychievements** is a framework for creating and tracking achievements within a Python application.
It includes functions specifically for creating commandline applications, though it is flexible 
enough to be used for any application such as web applications.

See the examples_ to get a good feel for what Pychievements offers. Docuementation can be found RTD:
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

    tracker.evluate(user_id, MyAchievement, some, extra, args)


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

Pychievements is licensed under the MIT License: ::

    Copyright (c) 2014, Brian Knobbs <brian@pktperception.org>

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.


Contribute
----------

If you'd like to contribute, simply fork `the repository`_, commit your changes
to the **master** branch (or branch off of it), and send a pull request. Make
sure you add yourself to AUTHORS_.


.. _`the repository`: http://github.com/PacketPerception/pychievements
.. _AUTHORS: http://github.com/PacketPerception/pychievements/blob/master/AUTHORS


Roadmap
-------
- Unittests
- Documentation


.. |docs| image:: https://readthedocs.org/projects/pychievements/badge/?version=latest
    :alt: Documentation Status
    :scale: 100%
    :target: http://pychievements.readthedocs.org/en/latest/
