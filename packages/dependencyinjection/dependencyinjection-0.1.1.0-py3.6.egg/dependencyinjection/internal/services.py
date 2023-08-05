#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017~2999 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import typing
from overload import overload
from .common import LifeTime, IValidator, IServiceProvider, IScopedFactory, ILock, FakeLock
from .scopedfactory import ScopedFactory
from .provider import ServiceProvider
from .descriptors import (
    Descriptor,
    CallableDescriptor,
    InstanceDescriptor,
    ServiceProviderDescriptor,
    MapDescriptor
)
from .validator import Validator
from .servicesmap import ServicesMap
from .lock import ThreadLock
from .param_type_resolver import ParameterTypeResolver


class Services:
    def __init__(self):
        self._services: typing.List[Descriptor] = []
        self._name_map: typing.Dict[str, type] = {}
        self.singleton(IValidator, Validator)
        self.singleton(ILock, FakeLock)

    def add(self, service_type: type, obj: (callable, type), lifetime: LifeTime):
        ''' register a singleton type. '''
        if not isinstance(service_type, type):
            raise TypeError('service_type must be a type')
        if not isinstance(lifetime, LifeTime):
            raise TypeError
        if callable(obj):
            self._services.append(CallableDescriptor(service_type, obj, lifetime))
        else:
            raise ValueError
        return self

    @overload
    def instance(self, service_type: type, obj: object):
        ''' register a singleton instance to service type. '''
        if not isinstance(obj, service_type):
            raise TypeError('obj must be {} type'.format(service_type))
        self._services.append(InstanceDescriptor(service_type, obj))
        return self

    @instance.add
    def instance(self, obj: object):
        return self.instance(type(obj), obj)

    @overload
    def singleton(self, service_type: type, obj: callable):
        ''' register a singleton type. '''
        return self.add(service_type, obj, LifeTime.singleton)

    @singleton.add
    def singleton(self, service_type: type):
        return self.singleton(service_type, service_type)

    @overload
    def scoped(self, service_type: type, obj: (callable, type)):
        ''' register a scoped type. '''
        return self.add(service_type, obj, LifeTime.scoped)

    @scoped.add
    def scoped(self, service_type: type):
        return self.scoped(service_type, service_type)

    @overload
    def transient(self, service_type: type, obj: (callable, type)):
        ''' register a transient type. '''
        return self.add(service_type, obj, LifeTime.transient)

    @transient.add
    def transient(self, service_type: type):
        return self.transient(service_type, service_type)

    def threadsafety(self):
        '''
        make all `LifeTime.singleton` service thread safety.
        '''
        self.scoped(ILock, ThreadLock)
        return self

    def map(self, service_type: type, target_service_type: type):
        '''
        map a service type to another service type.
        '''
        if not isinstance(service_type, type):
            raise TypeError('service_type must be a type')
        if not isinstance(target_service_type, type):
            raise TypeError('target_service_type must be a type')
        self._services.append(MapDescriptor(service_type, target_service_type))
        return self

    def bind(self, parameter_name: str, service_type: type):
        '''
        bind a parameter name to service type.
        so we can resolve parameter type when function does not has annotation.
        '''
        if not isinstance(parameter_name, str):
            raise TypeError('parameter_name must be a str')
        if not isinstance(service_type, type):
            raise TypeError('service_type must be a type')
        self._name_map[parameter_name] = service_type
        return self

    @property
    def decorator(self):
        return Decorator(self)

    def build(self) -> IServiceProvider:
        self.instance(ParameterTypeResolver(self._name_map))
        self.transient(IScopedFactory, ScopedFactory)
        self._services.append(ServiceProviderDescriptor())
        service_map = ServicesMap(self._services)
        return ServiceProvider(service_map=service_map)


class Decorator:
    def __init__(self, services: Services):
        self._services = services

    def instance(self, service_type: type=None):
        def func(obj):
            self._services.instance(service_type or type(obj), obj)
            return obj
        return func

    def singleton(self, service_type: type=None):
        def func(obj):
            if not isinstance(service_type or obj, type):
                raise TypeError('service type canbe ignore only args is a type.')
            self._services.singleton(service_type or obj, obj)
            return obj
        return func

    def scoped(self, service_type: type=None):
        def func(obj):
            if not isinstance(service_type or obj, type):
                raise TypeError('service type canbe ignore only args is a type.')
            self._services.scoped(service_type or obj, obj)
            return obj
        return func

    def transient(self, service_type: type=None):
        def func(obj):
            if not isinstance(service_type or obj, type):
                raise TypeError('service type canbe ignore only args is a type.')
            self._services.transient(service_type or obj, obj)
            return obj
        return func
