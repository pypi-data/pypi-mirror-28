# coding: utf8

import constants
import struct


# 这样pos就是定长的了，不用截断了
def unpack_pos(content):
    return struct.unpack(constants.POS_FMT, content)


def pack_pos(timestamp, offset):
    return struct.pack(constants.POS_FMT, timestamp, offset)
