# -*- coding: utf-8 -*-
import os
import logging
import json
import pkg_resources
try:
    # python3
    from builtins import str as basestring
except ImportError:
    # python2
    pass
from zope import component
from zope.interface import Interface


class ICommandProvider(Interface):
    """ Marker for pytest play command provider """


class PlayEngine(object):
    """ JSON executor """

    def __init__(self, request, variables):
        """ The executor should be initialized with:
            * **request**. A pytest ``request`` fixture that will be used
              for looking up other fixtures like ``navigation``
              and ``parametrizer_class``
            * **variables**. A dictionary that wil be used for parametrize
              commands
        """
        self.navigation = request.getfixturevalue('navigation')
        self.variables = variables
        self.parametrizer_class = request.getfixturevalue('parametrizer_class')
        self.logger = logging.getLogger()
        self.gsm = component.getGlobalSiteManager()

        self.register_plugins()

    def get_file_contents(self, *tokens):
        """ Return file contents """
        data = ''
        with open(
                os.path.join(*tokens),
                'r') as file_obj:
            data = file_obj.read()
        return data

    @property
    def parametrizer(self):
        """ Parametrizer engine """
        return self.parametrizer_class(self.variables)

    def _json_loads(self, data):
        """ If data is a string returns json dumps """
        if not isinstance(data, basestring):
            # if not dic reparametrize
            data = self.parametrizer.parametrize(json.dumps(data))
        return self.parametrizer.json_loads(data)

    def execute(self, data, extra_variables={}):
        """ Execute parsed json-like file contents """
        if extra_variables:
            self.update_variables(extra_variables)
        data = self._json_loads(data)
        steps = data['steps']
        for step in steps:
            self.execute_command(step)

    def execute_command(self, command, **kwargs):
        """ Execute single command """
        command = self._json_loads(command)
        command_type = command['type']
        provider_name = command.get('provider', 'default')
        command_provider = self.get_command_provider(provider_name)

        if command_provider is None:
            self.logger.error('Not supported provider %r', command)
            raise ValueError('Command not supported',
                             command_type,
                             provider_name)

        method_name = 'command_{0}'.format(command_type)

        method = getattr(command_provider, method_name, None)
        if method is None:
            self.logger.error('Not supported command %r', command)
            raise NotImplementedError(
                'Command not implemented', command_type, provider_name)
        self.logger.info('Executing command %r', command)
        try:
            return method(command, **kwargs)
        except Exception:
            self.logger.error('FAILED command %r', command)
            raise

    def update_variables(self, extra_variables):
        """ Update variables """
        self.variables.update(extra_variables)
        self.logger.debug("Variables updated %r", self.variables)

    # register commands
    def register_plugins(self):
        """ Auto register plugins and command providers"""
        for entrypoint in pkg_resources.iter_entry_points('playcommands'):
            plugin = entrypoint.load()
            self.register_command_provider(plugin, entrypoint.name)

    def register_command_provider(self, factory, name):
        """ Register command provider """
        self.gsm.registerUtility(
            factory(self),
            ICommandProvider,
            name,
        )

    def get_command_provider(self, name):
        """ Get command provider by name """
        return component.queryUtility(ICommandProvider, name=name)
