# encoding: utf-8
"""
pychievments.icons includes the :py:mod:`Icon` class as well as a number of pre-defined icons useful
for CLI applications.

* unicodeCheck
* unicdeCheckBox
* star

"""


class ColorCatcher(object):
    def __getattr__(self, name):
        return lambda s: s
try:
    from clint.textui import colored
except ImportError:
    colored = ColorCatcher()


class Icon(object):
    """
    Simple class to represent an ``Icon`` for an achievement. It provides to functions,
    ``achieved``, and ``unachieved``, which will return the displayable icon for the appropriate
    state.

    The base Icon class can be used without modification to create simple text Icons, e.g.:

    .. code-block:: python

        star = Icon(unachieved=' No ', achieved=' Yes ')

    """
    def __init__(self, unachieved='', achieved=''):
        self._unachieved = unachieved
        self._achieved = achieved

    def unachieved(self, tracked_id=None, achievement=None):
        """ Returns the unachieved icon """
        return self._unachieved

    def achieved(self, tracked_id=None, achievement=None):
        """ Returns the achieved icon """
        return self._achieved


############################################################################################
# Some built-in ASCII icons
unicodeCheckBox = Icon('\n\n    ☐  \n', '\n\n    ☑  \n')
unicodeCheck = Icon('\n\n    ✗  \n', '\n\n    ✓  \n')

############################################################################################
# Some built-in ASCII Art icons
star = Icon(colored.white("""           ..
          .88.
         .8  8.
 ........8    8........
  D88888       8888888
    .88          88~.
     ,88        88D
     88  88..88  88.
    D  88.    .88  D
   D 8.          .8 8
  .D.              .D.
"""), colored.yellow("""           ..
          .88.
         .8888.
 ........888888........
  D8888888888888888888
    .88888888888888~.
     ,888888888888D
     888888..888888.
    D8888.    .8888D
   D88.          .888
  .D.              .D.
"""))
