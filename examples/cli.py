#!/usr/bin/env python
"""
 A simple command line shell tool with achievements!

Requires the ``clint`` python library to be installed to use the ``pychievements.cli`` commands.
"""

import sys
import cmd
from pychievements import tracker, Achievement, icons
from pychievements.signals import receiver, goal_achieved, highest_level_achieved
from pychievements.cli import print_goal, print_goals_for_tracked


class TheLister(Achievement):
    """
    Create a simple Achievement with 4 goals that can be reached
    """
    name = 'The Lister'
    category = 'cli'
    keywords = ('cli', 'commands', 'ls')
    goals = (
        {'level': 5, 'name': 'Getting Interested',
         'icon': icons.star, 'description': 'Used `ls` 5 times'},
        {'level': 10, 'name': 'Peruser of lists',
         'icon': icons.star, 'description': 'Used `ls` 10 times'},
        {'level': 15, 'name': 'The listing master', 'icon': icons.star,
         'description': 'Used `ls` 15 times'},
        {'level': 20, 'name': 'All your lists are belong to us!',
         'icon': icons.star, 'description': 'Used `ls` 20 times'},
    )
# Achievements must be registered with the tracker before they can be used
tracker.register(TheLister)


class TheCreator(Achievement):
    """
    Achievements can have as many goals as they like
    """
    name = 'The Creator'
    category = 'cli'
    keywords = ('cli', 'commands', 'create', 'modifiers')
    goals = (
        {'level': 1, 'name': 'My First Creation',
         'icon': icons.unicodeCheck, 'description': 'and it\'s so beautiful....'},
        {'level': 5, 'name': 'Green thumb',
         'icon': icons.unicodeCheckBox, 'description': 'You\'ve created at least 5 objects!'},
        {'level': 10, 'name': 'Clever thinker',
         'icon': icons.star, 'description': 'More than 10 new creations are all because of you.'},
        {'level': 17, 'name': 'Almost an adult',
         'icon': icons.star, 'description': 'Just about 18.'},
        {'level': 15, 'name': 'True Inspiration',
         'icon': icons.star, 'description': 'Or did you steal your ideas for these 15 items? Hmm?'},
        {'level': 20, 'name': 'Divine Creator',
         'icon': icons.star, 'description': 'All the world bows to your divine inspiration.'},
    )

    def evaluate(self, old_objects, new_objects, *args, **kwargs):
        """ TheCreator uses evalute instead of increment so it can increment the level based on the
        number of objects created and not have to count each one. Remember, evalute must return the
        achieved achievements after evaluating. """
        self._current += new_objects - old_objects
        return self.achieved
tracker.register(TheCreator)


@receiver(goal_achieved)
def new_goal(tracked_id, achievement, goals, **kwargs):
    """
    We've setup some signal receivers so when a new goal has been reached we can print out a message
    to our user. It is possible to achieve more than one goal at once, though this will be called
    once for an achievement update.
    """
    for g in goals:
        print_goal(g, True)


@receiver(highest_level_achieved)
def check_if_all_completed(tracked_id, **kwargs):
    """
    Another signal reciever where we will check to see if any goals are unmet after we know we've
    achieved the highest level for a single achievement.
    """
    unachieved = []
    for a in tracker.achievements():
        unachieved += tracker.unachieved(tracked_id, a)
    if not unachieved:
        print('\n\nYou\'ve achieved the highest level of every achievement possible! Congrats!')


class MyCLIProgram(cmd.Cmd):
    """
    Simple command shell that lets us create objects and then list them. We're not performing
    multi-user tracking in our shell, so the tracked_id for all commands will just be 'userid'.
    """
    intro = 'The Achievement Oriented Command Line! Use ctrl+c to exit'
    prompt = '(do stuff) '

    def __init__(self, *args, **kwargs):
        cmd.Cmd.__init__(self, *args, **kwargs)
        self._objects = []

    def do_ls(self, arg):
        """ List created objects """
        for _ in self._objects:
            print(_)
        # every time we run 'ls', increment the level for TheListener
        tracker.increment('userid', TheLister)

    def do_create(self, arg):
        """ Create objects (e.g. create 1 2 3 4 5)"""
        old = len(self._objects)
        self._objects += arg.split()
        # Have TheCreator update our level based on the number of objects we just created
        tracker.evaluate('userid', TheCreator, old, len(self._objects))

    def do_remove(self, arg):
        """ Remove objects """
        for o in arg.split():
            if o in self._objects:
                self._objects.remove(o)

    def do_achievements(self, arg):
        """ List achievements. Can specify 'all' to see all achievements, or 'current' to see
        achievements currently working towards. Shows achieved achievements by default
        """
        showall = arg.lower() == 'all'
        current = arg.lower() == 'current'
        print('')
        print_goals_for_tracked('userid', achieved=True, unachieved=showall, only_current=current,
                                level=True)

    def do_exit(self, arg):
        sys.exit(0)

    def do_EOF(self, arg):
        sys.exit(0)

if __name__ == '__main__':
    MyCLIProgram().cmdloop()
