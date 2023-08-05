#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017~2999 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import yaml
from ..nodes import FileInfo

# pylint: disable=R0201,C0111

@FileInfo.register_format(__name__.split('.')[-1])
class YamlSerializer:

    def load(self, src: FileInfo, kwargs):
        return yaml.load(src.read_text(), **kwargs)

    def dump(self, src: FileInfo, obj, kwargs):
        return src.write_text(yaml.dump(obj, **kwargs), append=False)
