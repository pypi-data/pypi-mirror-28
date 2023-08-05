#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017~2999 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import json
from ..nodes import FileInfo

# pylint: disable=R0201,C0111

@FileInfo.register_format(__name__.split('.')[-1])
class JsonSerializer:

    def load(self, src: FileInfo, kwargs):
        return json.loads(src.read_text(), **kwargs)

    def dump(self, src: FileInfo, obj, kwargs):
        return src.write_text(json.dumps(obj, **kwargs), append=False)
