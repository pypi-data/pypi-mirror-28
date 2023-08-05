from unittest import TestCase
from mock import patch, Mock

from cloudshell.tg.breaking_point.helpers.context_utils import get_api, get_logger_with_thread_id


class TestContextUtils(TestCase):
    def setUp(self):
        pass

    @patch('cloudshell.tg.breaking_point.helpers.context_utils.CloudShellSessionContext')
    def test_get_api(self, cloudshell_session_context_class):
        api_instance = Mock()
        cloudshell_session_context_instance = Mock()
        cloudshell_session_context_instance.get_api.return_value = api_instance
        cloudshell_session_context_class.return_value = cloudshell_session_context_instance
        context = Mock()
        api = get_api(context)
        self.assertIs(api, api_instance)
        cloudshell_session_context_class.assert_called_once_with(context)
        cloudshell_session_context_instance.get_api.assert_called_once_with()

    @patch('cloudshell.tg.breaking_point.helpers.context_utils.LoggingSessionContext')
    @patch('cloudshell.tg.breaking_point.helpers.context_utils.threading')
    def test_get_api(self, threading, logging_session_context_class):
        logger_instance = Mock()
        child_instance = Mock()
        context = Mock()
        thread_mock = Mock()
        threading.currentThread.return_value = thread_mock
        thread_name = Mock()
        thread_mock.name = thread_name
        logging_session_context_class.get_logger_for_context.return_value = logger_instance
        logger_instance.getChild.return_value = child_instance
        handler_mock = Mock()
        filter_mock = Mock()
        level_mock = Mock()
        logger_instance.handlers = [handler_mock]
        logger_instance.filters = [filter_mock]
        logger_instance.level = level_mock
        child = get_logger_with_thread_id(context)
        self.assertIs(child, child_instance)
        logging_session_context_class.get_logger_for_context.assert_called_once_with(context)
        logger_instance.getChild.assert_called_once_with(thread_name)
        child_instance.addHandler.assert_called_once_with(handler_mock)
        child_instance.addFilter.assert_called_once_with(filter_mock)
        self.assertIs(child.level, logger_instance.level)
