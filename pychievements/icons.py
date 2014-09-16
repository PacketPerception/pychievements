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
# Some built-in unicode icons
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


# from http://www.chris.com/ascii/index.php?art=animals/birds%20(land)
_ROADRUNNER_STR = r"""
   .==,_
  .===,_`\
.====,_ ` \      .====,__
  .==-,`~. \           `:`.__,
    `~~=-.  \           /^^^
       `~~=. \         /
          `~. \       /
            ~. \____./
              `.=====)
           ___.--~~~--.__
 ___\.--~~~              ~~~---.._|/
 ~~~"                             /
                                  '
"""
roadrunner = Icon(colored.white(_ROADRUNNER_STR), colored.yellow(_ROADRUNNER_STR))

_EAGLE_STR = r"""
            ___
         ,-'   >---.        ,---.
        /  ,o)'     `.     /     `.
       '|    (   ,_   )   |        `.
     ,--|    -.,'  `./    ;        `.
    /   |      `.         :   .      `
   /    |:.      `-       ,    \    :.\\
  |   ,-|'        \-.___,'     :\   ;::\\
  |, ::'\   ,      `.        ,.::\   :(-
  |: |:; \,'\  ).   / .:..  ,:::::\   `\\
  |  |,:  `  `/  `-/ ::::::::::::::\    ;
  |   |:             ::::::::::::::.\   |
  \   |:.,           ::::::::::   ` |;  |
   \  `.:'       ::.,::::::: `:  \  ||  |
    \   \     . ,:::::::,:::  . ( `-'|  |
     `.  \     ::::,`':(::' ` |\ \   :  |
       \  :-:. `::      \ `   | \ \   \ |
        `'  |:' `'  /`.  `. \ :  `'    \|
           /   \    \ `._/ `'`-`        |
       __ / \, ,\   _\\  `.
     _/ ,\- (`'  `-',-','-,"-.
    /,-(,- \_\     (-'(,---.:.)
"""
eagle = Icon(colored.white(_EAGLE_STR), colored.yellow(_EAGLE_STR))


_BEE_STR = r"""

                             ...vvvv)))))).
  /~~\               ,,,c(((((((((((((((((/
 /~~c \.         .vv)))))))))))))))))))\``
     G_G__   ,,(((KKKK//////////////'
   ,Z~__ '@,gW@@AKXX~MW,gmmmz==m_.
  iP,dW@!,A@@@@@@@@@@@@@@@A` ,W@@A\c
  ]b_.__zf !P~@@@@@*P~b.~+=m@@@*~ g@Ws.
     ~`    ,2W2m. '\[ ['~~c'M7 _gW@@A`'s
       v=XX)====Y-  [ [    \c/*@@@*~ g@@i
      /v~           !.!.     '\c7+sg@@@@@s.
     //              'c'c       '\c7*X7~~~~
    ]/                 ~=Xm_       '~=(Gm_.
"""
bee = Icon(colored.white(_BEE_STR), colored.yellow(_BEE_STR))

_EARTH_STR = r"""
                 ,,,,,,
             o#'9MMHb':'-,o,
          .oH":HH$' "' ' -*R&o,
         dMMM*""'`'      .oM"HM?.
       ,MMM'          "HLbd< ?&H\\
      .:MH ."\          ` MM  MM&b
     . "*H    -        &MMMMMMMMMH:
     .    dboo        MMMMMMMMMMMM.
     .   dMMMMMMb      *MMMMMMMMMP.
     .    MMMMMMMP        *MMMMMP .
          `#MMMMM           MM6P ,
      '    `MMMP"           HM*`,
       '    :MM             .- ,
        '.   `#?..  .       ..'
           -.   .         .-
             ''-.oo,oo.-''
"""
earth = Icon(colored.white(_EARTH_STR), colored.yellow(_EARTH_STR))

book = Icon(colored.white("""
        _.-"\\
    _.-"     \\
 ,-"          \\
( \            \\
 \ \            \\
  \ \            \\
   \ \         _.-;
    \ \    _.-"   :
     \ \,-"    _.-"
      \(   _.-"
       `--"
"""), colored.yellow("""
      _.--._  _.--._
,-=.-":;:;:;\':;:;:;"-._
\\\:;:;:;:;:;\:;:;:;:;:;\\
 \\\:;:;:;:;:;\:;:;:;:;:;\\
  \\\:;:;:;:;:;\:;:;:;:;:;\\
   \\\:;:;:;:;:;\:;::;:;:;:\\
    \\\;:;::;:;:;\:;:;:;::;:\\
     \\\;;:;:_:--:\:_:--:_;:;\\
      \\\_.-"      :      "-._\\
       \`_..--"--.;.--""--.._=>
"""))
