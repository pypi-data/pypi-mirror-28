#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017~2999 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from abc import abstractmethod, abstractproperty
from enum import Enum


class LifeTime(Enum):
    singleton = 0
    scoped = 1
    transient = 2


class IServiceProvider:
    def get(self, service_type: type):
        '''
        get service by the type.
        '''
        raise NotImplementedError

    def scope(self):
        '''
        get a scoped `IServiceProvider`.

        usage:
        ``` py
        with ?.scope() as service_provider:
            obj = service_provider.get(?)
        ```
        '''
        raise NotImplementedError


class ICallSiteMaker:
    @abstractmethod
    def make_callsite(self, service_provider: IServiceProvider, depend_chain):
        '''create a callsite.'''
        raise NotImplementedError


class IDescriptor(ICallSiteMaker):

    @abstractproperty
    def service_type(self) -> type:
        raise NotImplementedError

    @abstractproperty
    def lifetime(self) -> LifeTime:
        raise NotImplementedError


class IScopedFactory:
    @property
    def service_provider(self):
        raise NotImplementedError


class ILock:
    ''' the lock use for scoped service provider. '''

    @abstractmethod
    def __enter__(self):
        raise NotImplementedError

    @abstractmethod
    def __exit__(self, exc_type, exc_value, traceback):
        raise NotImplementedError


class FakeLock(ILock):
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

FAKE_LOCK = FakeLock()
