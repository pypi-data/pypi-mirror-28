from unittest import TestCase

from mock import Mock, patch, PropertyMock

from cloudshell.tg.breaking_point.runners.bp_runner import BPRunner


class BPRunnerImpl(BPRunner):
    pass


class TestBPRunner(TestCase):
    def setUp(self):
        self.__context = Mock()
        self.__api = Mock()
        self.__logger = Mock()
        self.__session_context_manager = Mock()
        self.__instance = None

    @property
    def _instance_with_session_context_manager(self):
        if not self.__instance:
            self.__instance = BPRunnerImpl(self.__context, self.__logger, self.__api, self.__session_context_manager)
        return self.__instance

    @property
    def _instance_without_session_context_manager(self):
        if not self.__instance:
            self.__instance = BPRunnerImpl(self.__context, self.__logger, self.__api)
        return self.__instance

    def test_context_getter(self):
        self.assertIs(self._instance_without_session_context_manager.context, self.__context)

    @patch('cloudshell.tg.breaking_point.runners.bp_runner.BPRunner._username', new_callable=PropertyMock)
    @patch('cloudshell.tg.breaking_point.runners.bp_runner.BPRunner._password', new_callable=PropertyMock)
    @patch('cloudshell.tg.breaking_point.runners.bp_runner.BPRunner._resource_address', new_callable=PropertyMock)
    def test_context_setter(self, resource_address_prop,
                            password_prop, username_prop):
        new_context = Mock()
        resource_address = Mock()
        resource_address_prop.return_value = resource_address
        username = Mock()
        username_prop.return_value = username
        password = Mock()
        password_prop.return_value = password
        self._instance_with_session_context_manager.context = new_context
        self.assertIs(new_context, self._instance_with_session_context_manager.context)
        self.assertIs(resource_address, self.__session_context_manager.hostname)
        self.assertIs(username, self.__session_context_manager.username)
        self.assertIs(password, self.__session_context_manager.password)

    def test_logger_getter(self):
        self.assertIs(self._instance_without_session_context_manager.logger, self.__logger)

    def test_logger_setter(self):
        new_logger = Mock()
        self._instance_with_session_context_manager.logger = new_logger
        self.assertIs(new_logger, self._instance_with_session_context_manager.logger)
        self.assertIs(new_logger, self.__session_context_manager.logger)

    def test_api_getter(self):
        self.assertIs(self.__api, self._instance_with_session_context_manager.api)

    def test_api_setter(self):
        new_api = Mock()
        self._instance_with_session_context_manager.api = new_api
        self.assertIs(new_api, self._instance_with_session_context_manager.api)

    @patch('cloudshell.tg.breaking_point.runners.bp_runner.get_attribute_by_name')
    def test_username_getter(self, get_attribute_by_name):
        username = Mock()
        get_attribute_by_name.return_value = username
        self.assertIs(self._instance_with_session_context_manager._username, username)
        get_attribute_by_name.assert_called_once_with('User', self.__context)

    @patch('cloudshell.tg.breaking_point.runners.bp_runner.get_attribute_by_name')
    def test_password_getter(self, get_attribute_by_name):
        password = Mock()
        get_attribute_by_name.return_value = password
        value = Mock()
        value.Value = Mock()
        self.__api.DecryptPassword.return_value = value
        self.assertIs(self._instance_with_session_context_manager._password, value.Value)
        get_attribute_by_name.assert_called_once_with('Password', self.__context)
        self.__api.DecryptPassword.assert_called_once_with(password)

    @patch('cloudshell.tg.breaking_point.runners.bp_runner.get_resource_address')
    def test_resource_address_getter(self, get_resource_address):
        resource_address = Mock()
        get_resource_address.return_value = resource_address
        self.assertIs(resource_address, self._instance_with_session_context_manager._resource_address)
        get_resource_address.assert_called_once_with(self.__context)

    def test_session_context_manager_getter_created_instance(self):
        self.assertIs(self.__session_context_manager,
                      self._instance_with_session_context_manager._session_context_manager)

    @patch('cloudshell.tg.breaking_point.runners.bp_runner.BPRunner._username', new_callable=PropertyMock)
    @patch('cloudshell.tg.breaking_point.runners.bp_runner.BPRunner._password', new_callable=PropertyMock)
    @patch('cloudshell.tg.breaking_point.runners.bp_runner.BPRunner._resource_address', new_callable=PropertyMock)
    @patch('cloudshell.tg.breaking_point.runners.bp_runner.RestSessionContextManager')
    def test_session_context_manager_getter_create_instance(self, session_context_manager_class, resource_address_prop,
                                                            password_prop, username_prop):
        resource_address = Mock()
        resource_address_prop.return_value = resource_address
        username = Mock()
        username_prop.return_value = username
        password = Mock()
        password_prop.return_value = password
        instance = Mock()
        session_context_manager_class.return_value = instance
        self.assertIs(instance, self._instance_without_session_context_manager._session_context_manager)
        session_context_manager_class.assert_called_once_with(resource_address, username, password, self.__logger)
