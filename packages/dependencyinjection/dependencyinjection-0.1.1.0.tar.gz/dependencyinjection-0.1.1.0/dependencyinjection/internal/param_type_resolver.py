#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017~2999 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import typing
import inspect
from .errors import ParameterTypeResolveError

class ParameterTypeResolver:
    ''' desgin for resolve type from parameter. '''

    def __init__(self, name_map: typing.Dict[str, type]):
        self._name_map = name_map.copy()

    def resolve(self, parameter: inspect.Parameter):
        if parameter.annotation is inspect.Parameter.empty:
            t = self._name_map.get(parameter.name)
            if t is None:
                msg = "cannot resolve parameter type by name: '{}'".format(parameter.name)
                raise ParameterTypeResolveError(msg)
            return t
        elif isinstance(parameter.annotation, type):
            return parameter.annotation
        else:
            msg = 'cannot parse type from annotation: {}'.format(parameter.annotation)
            raise ParameterTypeResolveError(msg)

