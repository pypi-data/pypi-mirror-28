#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017~2999 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import typing
import colorama
from .colors import (
    lightred,
    lightgreen
)

colorama.init()

class Stop(Exception):
    ''' user selected terminate application without show any message. '''
    pass

class Help(Exception):
    ''' user selected print help message.'''
    pass

REQUIRE_SUFFIX = ': '

class Option:
    def __init__(self, name: str, keys: typing.List[str], value):
        self._name = name
        self._keys = tuple(keys)
        self._value = value

    @property
    def name(self):
        return self._name

    @property
    def keys(self):
        return self._keys

    @property
    def value(self):
        return self._value

    def styled_text(self, isdef: bool):
        text = self._name
        if self._keys[0] != self._name:
            text = '[{k}] {n}'.format(k=self._keys[0].upper(), n=self._name)
        if isdef:
            text = lightgreen(text)
        return text

    def invoke(self):
        return self._value


class ExceptionOption(Option):
    def invoke(self):
        raise self._value


class Picker:
    def __init__(self, sep: str):
        self._sep = sep
        self._items: typing.List[Option] = []
        self._table: typing.Dict[str, Option] = {}

    def add(self, option: Option):
        for k in option.keys:
            kl = k.lower()
            e = self._table.get(kl)
            if e:
                raise ValueError('key <{}> is two option: <{}> and <{}>'.format(k, e.name, option.name))
            self._table[kl] = option
        self._items.append(option)

    def get_styled_text(self, defval):
        def_option = None
        for o in self._items:
            if o.value == defval:
                def_option = o
                break
        text = self._sep.join(o.styled_text(o is def_option) for o in self._items)
        if def_option:
            text += self._sep + '(default value is {})'.format(def_option.name)

        text += self._sep + REQUIRE_SUFFIX
        return text

    def pick(self, defval):
        print(self.get_styled_text(defval), end='')
        rawvalue = input()
        value = rawvalue.lower()
        option = self._table.get(value)
        if option is not None:
            return option.invoke()
        if value == '':
            return defval
        else:
            msg = '{} is valid input'.format(rawvalue)
            print(lightred(msg))
            return self.pick(defval)
