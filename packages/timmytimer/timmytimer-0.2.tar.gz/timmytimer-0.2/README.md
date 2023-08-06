# Timmytimer
Named after the childrens TV-show Timmy Time

A simple wrapper to log/print functionname, \*args and \**kwargs and how long it took to execute

## INSTALL
pip install timmytimer


## Example Usage

```python
from timmytimer import timmy, timmyp, timmyprint
import logging
from time import sleep
from random import random

# *if* you have installed colorama you get colored print
try:
    from colorama import Fore, Back, Style, init
    init(autoreset=True)
except ImportError:  # fallback so that the imported classes always exist
    class ColorFallback():
        __getattr__ = lambda self, name: ''
    Fore = Back = Style = ColorFallback()

@timmy
def test_timmy(greeting, name='Henrik'):
    sleep(random())
    print('{} {}'.format(greeting, name))

@timmyprint
def test_timmyprint(greeting, name='Henrik'):
    sleep(random())
    print('{} {}'.format(greeting, name))

@timmyp
def test_timmyp(greeting, name='Henrik'):
    sleep(random())
    print('{} {}'.format(greeting, name))


if __name__ == '__main__':
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)

    test_timmy('Hello', name='Gustav')
    test_timmyprint('Goodday', name='Ellinor')
    test_timmyp('P-man')
```

output:
```console
(wenv) C:\Users\henrik\Desktop\git_temp\timmytimer>py tests\test.py
Hello Gustav
DEBUG:root:[timmytimer]test_timmy(('Hello',){'name': 'Gustav'})370.00ms
Goodday Ellinor
[timmytimer] test_timmyprint(('Goodday',){'name': 'Ellinor'}) 536.00ms
P-man Henrik
[timmytimer] test_timmyp(('P-man',){}) 230.00ms
```
