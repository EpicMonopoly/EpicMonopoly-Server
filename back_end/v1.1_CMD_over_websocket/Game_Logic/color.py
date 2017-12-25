from enum import Enum, unique


@unique
class Color(Enum):
    empty = 0xeeeeee
    blue = 0x3399ff
    red = 0xbb0407
    yellow = 0xfdb515
    purple = 0xbf3eff
    green = 0x8dc63f
    dark = 0x430a0a
    pink = 0xff6666
