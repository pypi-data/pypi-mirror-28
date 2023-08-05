#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017~2999 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import os

class PathPart(str):
    def __init__(self, val):
        if not isinstance(val, str):
            raise TypeError
        self._val = val
        self._normcased = os.path.normcase(val)

    def __repr__(self):
        return '{}(\'{}\')'.format(type(self).__name__, self)

    @property
    def normalcase(self):
        ''' return normcase path which create from `os.path.normcase()`. '''
        return self._normcased

    def equals(self, other):
        ''' compare with `os.path.normcase()` '''
        return self._normcased == os.path.normcase(other)


class NamePart(PathPart):
    def __init__(self, val):
        super().__init__(val)
        self._pure_name = None
        self._ext = None

    def __ensure_pure_name(self):
        if self._pure_name is None:
            pn, ext = os.path.splitext(self)
            self._pure_name = PathPart(pn)
            self._ext = PathPart(ext)

    @property
    def pure_name(self) -> PathPart:
        ''' get name without ext from path. '''
        self.__ensure_pure_name()
        return self._pure_name

    @property
    def ext(self) -> PathPart:
        ''' get ext from path. '''
        self.__ensure_pure_name()
        return self._ext

    def replace_pure_name(self, val):
        if not isinstance(val, str):
            raise TypeError
        return NamePart(val + self.ext)

    def replace_ext(self, val):
        if not isinstance(val, str):
            raise TypeError
        return NamePart(self.pure_name + val)


class Path(PathPart):
    def __init__(self, val):
        super().__init__(val)
        self._dirname = None
        self._name = None

    def __ensure_dirname(self):
        if self._dirname is None:
            dn, fn = os.path.split(self)
            self._dirname = Path(dn)
            self._name = NamePart(fn)

    @property
    def dirname(self):
        ''' get directory path from path. '''
        self.__ensure_dirname()
        return self._dirname

    @property
    def name(self) -> NamePart:
        ''' get name from path. '''
        self.__ensure_dirname()
        return self._name

    @property
    def pure_name(self) -> PathPart:
        ''' get name without ext from path. '''
        return self.name.pure_name

    @property
    def ext(self) -> PathPart:
        ''' get ext from path. '''
        return self.name.ext

    def is_ext_equals(self, val):
        ''' use `self.ext.equals()` instead。 '''
        return self.ext.equals(val)

    def replace_dirname(self, val):
        if not isinstance(val, str):
            raise TypeError
        return Path(os.path.join(val, self.name))

    def replace_name(self, val):
        if not isinstance(val, str):
            raise TypeError
        return Path(os.path.join(self.dirname, val))

    def replace_pure_name(self, val):
        return Path(os.path.join(self.dirname, self.name.replace_pure_name(val)))

    def replace_ext(self, val):
        return Path(os.path.join(self.dirname, self.name.replace_ext(val)))
