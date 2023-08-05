from abc import ABCMeta
from cloudshell.shell.core.context_utils import get_attribute_by_name, get_resource_address
from cloudshell.tg.breaking_point.rest_api.rest_session_manager import RestSessionContextManager


class BPRunner(object):
    __metaclass__ = ABCMeta

    def __init__(self, context, logger, api, session_context_manager=None):
        self.__context = context
        self.__api = api
        self.__logger = logger

        self.__session_context_manager = session_context_manager

    @property
    def context(self):
        return self.__context

    @context.setter
    def context(self, value):
        self.__context = value
        if self.__session_context_manager:
            self.__session_context_manager.hostname = self._resource_address
            self.__session_context_manager.username = self._username
            self.__session_context_manager.password = self._password

    @property
    def logger(self):
        return self.__logger

    @logger.setter
    def logger(self, value):
        self.__logger = value
        if self.__session_context_manager:
            self.__session_context_manager.logger = value

    @property
    def api(self):
        return self.__api

    @api.setter
    def api(self, value):
        self.__api = value

    def _get_attribute_by_name(self, attribute):
        full_attribute_name = attribute
        if self.context.resource.family == 'CS_TrafficGeneratorChassis':
            full_attribute_name = self.context.resource.model + '.' + full_attribute_name
        return get_attribute_by_name(full_attribute_name, self.context)

    @property
    def _username(self):
        return self._get_attribute_by_name('User')

    @property
    def _password(self):
        return self.api.DecryptPassword(self._get_attribute_by_name('Password')).Value

    @property
    def _resource_address(self):
        """Resource IP

        :return:
        """
        return get_resource_address(self.context)

    @property
    def _session_context_manager(self):
        if not self.__session_context_manager:
            self.__session_context_manager = RestSessionContextManager(self._resource_address, self._username,
                                                                       self._password,
                                                                       self.logger)
        return self.__session_context_manager
