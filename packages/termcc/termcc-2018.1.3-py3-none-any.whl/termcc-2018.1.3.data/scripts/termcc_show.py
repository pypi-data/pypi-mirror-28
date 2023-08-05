#!python
from termcc.cc import cc

from termcc.core import red, blue_, reset

print('cc by dameng :P')


def show():
    # print('test')
    print(red()+'hello world'+reset())
    print(cc(':yin_yang:'))
    print(cc(':red: :yin_yang: :reverse_green: hello world'))


if __name__ == '__main__':
    show()
