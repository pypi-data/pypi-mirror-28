#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017~2999 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import os
import io
from .common import Option, ExceptionOption, Picker, Stop, Help

def pick_method(obj: object, *,
        allow_none: bool=True,
        raise_on_help: bool=True,
        include_doc: bool=True) -> callable:
    '''
    pick a method from a obj (`cls` or `self`).
    can use filter to filter

    return `None` if user pick `None`.
    '''
    if obj is None:
        raise ValueError('obj cannot be None')

    is_class = isinstance(obj, type)
    methods = []
    for name in dir(obj):
        if name.startswith('_'):
            continue
        attr = getattr(obj, name)
        if is_class:
            if isinstance(vars(obj).get(name), (staticmethod, classmethod)):
                methods.append((name, attr))
        else:
            if callable(attr):
                methods.append((name, attr))

    lwidths = []
    for idx, (name, method) in enumerate(methods):
        len_of_name = len(name)
        len_of_name = max(4, len_of_name)
        len_of_idx = len(str(idx)) + 3
        lwidths.append((len_of_idx, len_of_name + 4))
    mkw = max(lwidths, key=lambda x: x[0] + x[1])
    wincol = os.get_terminal_size().columns - 20
    doccol = wincol - mkw[0] - mkw[1]

    options = Picker(sep='\n')
    for idx, (name, method) in enumerate(methods):
        doc = getattr(method, '__doc__', '')

        if not doc or doccol <= 10 or not include_doc:
            desc = name

        else:
            sio = io.StringIO()
            sio.write(name.ljust(mkw[1]))
            def write_newline():
                sio.write('\n')
                sio.write(' ' * (mkw[0] + mkw[1]))
            for lineno, line in enumerate(doc.strip().splitlines()):
                if lineno > 0:
                    write_newline()
                i = 0
                for ch in line.strip():
                    if i >= doccol:
                        write_newline()
                        i = 0
                    sio.write(ch)
                    i += 1

            desc = sio.getvalue()

        options.add(Option(desc, [str(idx), name], method))

    if allow_none:
        options.add(Option('None', ['X', 'none'], None))
    options.add(ExceptionOption('Stop', ['S', 'stop'], Stop))
    if raise_on_help:
        options.add(ExceptionOption('Help', ['?', 'H'], Help))
    else:
        options.add(Option('Help', ['?', 'H'], Help))
    return options.pick(None)
