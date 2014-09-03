"""

Pychievements!

The Python achievements framework!!

"""

from __future__ import absolute_import

from .trackers import AchievementTracker
from .achievements import Achievement
tracker = AchievementTracker()

__all__ = ['tracker', 'Achievement']


__title__ = 'pychievements'
__version__ = '0.1.2'
__build__ = 0x000102
__auther__ = 'Brian Knobbs'
__license__ = 'MIT'
__copyright__ = 'Copyright 2014 Brian Knobbs'
__docformat__ = 'restructuredtext'
