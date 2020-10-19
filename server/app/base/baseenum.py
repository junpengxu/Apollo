# -*- coding: utf-8 -*-
# @Time    : 2020/10/20 1:02 上午
# @Author  : xu.junpeng

from enum import Enum


class EnumBase(Enum):

    @property
    def code(self):
        return self.value

    @code.getter
    def code(self):
        return self.value[0]

    @property
    def desc(self):
        return self.value

    @desc.getter
    def desc(self):
        return self.value[1]
