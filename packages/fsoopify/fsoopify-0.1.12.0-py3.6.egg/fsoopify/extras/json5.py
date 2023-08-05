#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017~2999 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import json5
from ..nodes import FileInfo

# pylint: disable=R0201,C0111

@FileInfo.register_format(__name__.split('.')[-1])
class Json5Serializer:

    def load(self, src: FileInfo):
        return json5.loads(src.read_text())

    def dump(self, src: FileInfo, obj):
        return src.write_text(json5.dumps(obj), append=False)
