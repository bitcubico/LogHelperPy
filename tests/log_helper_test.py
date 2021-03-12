import unittest

from log_helper import LogHelper


class MyTestCase(unittest.TestCase):
    DEBUG_MESSAGE = 'Mensaje de tipo debug'
    INFO_MESSAGE = 'Mensaje de tipo info'
    WARNING_MESSAGE = 'Mensaje de tipo warning'
    ERROR_MESSAGE = 'Mensaje de tipo error'
    FATAL_MESSAGE = 'Mensaje de tipo fatal'

    def test_add_debug_log_to_list(self):
        log = LogHelper()
        log.debug(self.DEBUG_MESSAGE)

        self.assertEqual(log.logs.__len__() == 1 and log.logs[0].log_level == LogHelper.DEBUG, True)

    def test_add_info_log_to_list(self):
        log = LogHelper()
        log.info(self.INFO_MESSAGE)

        self.assertEqual(log.logs.__len__() == 1 and log.logs[0].log_level == LogHelper.INFO, True)

    def test_add_warning_log_to_list(self):
        log = LogHelper()
        log.warning(self.WARNING_MESSAGE)

        self.assertEqual(log.logs.__len__() == 1 and log.logs[0].log_level == LogHelper.WARNING, True)

    def test_add_error_log_to_list(self):
        log = LogHelper()
        log.error(self.ERROR_MESSAGE)

        self.assertEqual(log.logs.__len__() == 1 and log.logs[0].log_level == LogHelper.ERROR, True)

    def test_add_fatal_log_to_list(self):
        log = LogHelper()
        log.fatal(self.FATAL_MESSAGE)

        self.assertEqual(log.logs.__len__() == 1 and log.logs[0].log_level == LogHelper.FATAL, True)

    def test_not_add_log_to_list_if_message_is_empty(self):
        log = LogHelper()
        log.debug('')
        log.debug('  ')

        self.assertEqual(log.logs.__len__() == 0, True)

    def test_print_in_file_all_logs(self):
        log = LogHelper()

        log.debug(self.DEBUG_MESSAGE)
        log.info(self.INFO_MESSAGE)
        log.warning(self.WARNING_MESSAGE)
        log.error(self.ERROR_MESSAGE)
        log.fatal(self.FATAL_MESSAGE)

        log_name = 'test_print_in_file_all_logs.log'
        self.assertTrue(log.logs.__len__() == 5)
        self.assertEqual(log.save_logs(log_name, log_level=LogHelper.DEBUG), True)
        with open(f'./{log_name}') as file:
            data = file.read()
            self.assertTrue(self.DEBUG_MESSAGE in data)
            self.assertTrue(self.INFO_MESSAGE in data)
            self.assertTrue(self.WARNING_MESSAGE in data)
            self.assertTrue(self.ERROR_MESSAGE in data)
            self.assertTrue(self.FATAL_MESSAGE in data)

    def test_print_in_file_exceptions_log(self):
        log = LogHelper()
        exception = Exception('Excepción test')
        log.error(exception)
        try:
            1 / 0
        except Exception as ex:
            log.fatal(ex)

        log_name = 'test_print_in_file_exceptions_log.log'
        self.assertTrue(log.logs.__len__() == 2)
        self.assertEqual(log.save_logs(log_name, log_level=LogHelper.DEBUG), True)
        with open(f'./{log_name}') as file:
            data = file.read()
            self.assertTrue(exception.__str__() in data)
            self.assertTrue('division by zero' in data)

    def test_print_in_file_only_info_or_higher_levels(self):
        log = LogHelper()

        log.debug(self.DEBUG_MESSAGE)
        log.info(self.INFO_MESSAGE)
        log.warning(self.WARNING_MESSAGE)
        log.error(self.ERROR_MESSAGE)
        log.fatal(self.FATAL_MESSAGE)

        log_name = 'test_print_in_file_only_info_or_higher_levels.log'
        self.assertTrue(log.logs.__len__() == 5)
        self.assertEqual(log.save_logs(log_name, log_level=LogHelper.INFO), True)
        with open(f'./{log_name}') as file:
            data = file.read()
            self.assertFalse(self.DEBUG_MESSAGE in data)
            self.assertTrue(self.INFO_MESSAGE in data)
            self.assertTrue(self.WARNING_MESSAGE in data)
            self.assertTrue(self.ERROR_MESSAGE in data)
            self.assertTrue(self.FATAL_MESSAGE in data)

    def test_print_in_file_only_error_or_higher_levels(self):
        log = LogHelper()

        log.debug(self.DEBUG_MESSAGE)
        log.info(self.INFO_MESSAGE)
        log.warning(self.WARNING_MESSAGE)
        log.error(self.ERROR_MESSAGE)
        log.fatal(self.FATAL_MESSAGE)

        log_name = 'test_print_in_file_only_error_or_higher_levels.log'
        self.assertTrue(log.logs.__len__() == 5)
        self.assertEqual(log.save_logs(log_name, log_level=LogHelper.ERROR), True)
        with open(f'./{log_name}') as file:
            data = file.read()
            self.assertFalse(self.DEBUG_MESSAGE in data)
            self.assertFalse(self.INFO_MESSAGE in data)
            self.assertFalse(self.WARNING_MESSAGE in data)
            self.assertTrue(self.ERROR_MESSAGE in data)
            self.assertTrue(self.FATAL_MESSAGE in data)

    def test_add_external_logs(self):
        log = LogHelper()
        external_logs = LogHelper()

        log.debug(self.DEBUG_MESSAGE)
        log.info(self.INFO_MESSAGE)
        log.warning(self.WARNING_MESSAGE)
        log.error(self.ERROR_MESSAGE)
        log.fatal(self.FATAL_MESSAGE)

        external_msg_debug = 'Mensaje de debug externo'
        external_msg_info = 'Mensaje de info externo'
        external_msg_warning = 'Mensaje de warning externo'
        external_msg_error = 'Mensaje de error externo'
        external_msg_fatal = 'Mensaje de fatal externo'

        external_logs.debug(external_msg_debug)
        external_logs.info(external_msg_info)
        external_logs.warning(external_msg_warning)
        external_logs.error(external_msg_error)
        external_logs.fatal(external_msg_fatal)

        log.add_external_logs(external_logs.logs)
        self.assertTrue(log.logs.__len__() == 10)

        log_name = 'test_add_external_logs.log'
        self.assertEqual(log.save_logs(log_name, log_level=LogHelper.DEBUG), True)
        with open(f'./{log_name}') as file:
            data = file.read()
            self.assertTrue(self.DEBUG_MESSAGE in data)
            self.assertTrue(self.INFO_MESSAGE in data)
            self.assertTrue(self.WARNING_MESSAGE in data)
            self.assertTrue(self.ERROR_MESSAGE in data)
            self.assertTrue(self.FATAL_MESSAGE in data)

            self.assertTrue(external_msg_debug in data)
            self.assertTrue(external_msg_info in data)
            self.assertTrue(external_msg_warning in data)
            self.assertTrue(external_msg_error in data)
            self.assertTrue(external_msg_fatal in data)

    def test_not_add_logs_that_do_not_comply_with_the_data_types(self):
        log = LogHelper()

        log.debug(self.DEBUG_MESSAGE)
        log.info(self.INFO_MESSAGE)
        log.warning(self.WARNING_MESSAGE)
        log.error(self.ERROR_MESSAGE)
        log.fatal(self.FATAL_MESSAGE)

        log.add_external_logs([1, 2, 3, 'uno', 'dos'])
        log.add_external_logs('datos')
        self.assertTrue(log.logs.__len__() == 5)


if __name__ == '__main__':
    unittest.main()
