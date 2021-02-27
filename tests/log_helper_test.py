import unittest

from log_helper import LogHelper


class MyTestCase(unittest.TestCase):
    debug_message = 'Mensaje de tipo debug'
    info_message = 'Mensaje de tipo info'
    warning_message = 'Mensaje de tipo warning'
    error_message = 'Mensaje de tipo error'
    fatal_message = 'Mensaje de tipo fatal'

    def test_add_debug_log_to_list(self):
        log = LogHelper()
        log.debug(self.debug_message)

        self.assertEqual(log.logs.__len__() == 1 and log.logs[0].log_level == LogHelper.DEBUG, True)

    def test_add_info_log_to_list(self):
        log = LogHelper()
        log.info(self.info_message)

        self.assertEqual(log.logs.__len__() == 1 and log.logs[0].log_level == LogHelper.INFO, True)

    def test_add_warning_log_to_list(self):
        log = LogHelper()
        log.warning(self.warning_message)

        self.assertEqual(log.logs.__len__() == 1 and log.logs[0].log_level == LogHelper.WARNING, True)

    def test_add_error_log_to_list(self):
        log = LogHelper()
        log.error(self.error_message)

        self.assertEqual(log.logs.__len__() == 1 and log.logs[0].log_level == LogHelper.ERROR, True)

    def test_add_fatal_log_to_list(self):
        log = LogHelper()
        log.fatal(self.fatal_message)

        self.assertEqual(log.logs.__len__() == 1 and log.logs[0].log_level == LogHelper.FATAL, True)

    def test_not_add_log_to_list_if_message_is_empty(self):
        log = LogHelper()
        log.debug('')
        log.debug('  ')

        self.assertEqual(log.logs.__len__() == 0, True)

    def test_print_in_file_all_logs(self):
        log = LogHelper()

        log.debug(self.debug_message)
        log.info(self.info_message)
        log.warning(self.warning_message)
        log.error(self.error_message)
        log.fatal(self.fatal_message)

        log_name = 'test_print_in_file_all_logs.log'
        self.assertTrue(log.logs.__len__() == 5)
        self.assertEqual(log.save_logs(log_name, log_level=LogHelper.DEBUG), True)
        with open(f'./{log_name}') as file:
            data = file.read()
            self.assertTrue(self.debug_message in data)
            self.assertTrue(self.info_message in data)
            self.assertTrue(self.warning_message in data)
            self.assertTrue(self.error_message in data)
            self.assertTrue(self.fatal_message in data)

    def test_print_in_file_exceptions_log(self):
        log = LogHelper()
        exception = Exception('Excepción test')
        log.error(exception)
        try:
            data = 1/0
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

        log.debug(self.debug_message)
        log.info(self.info_message)
        log.warning(self.warning_message)
        log.error(self.error_message)
        log.fatal(self.fatal_message)

        log_name = 'test_print_in_file_only_info_or_higher_levels.log'
        self.assertTrue(log.logs.__len__() == 5)
        self.assertEqual(log.save_logs(log_name, log_level=LogHelper.INFO), True)
        with open(f'./{log_name}') as file:
            data = file.read()
            self.assertFalse(self.debug_message in data)
            self.assertTrue(self.info_message in data)
            self.assertTrue(self.warning_message in data)
            self.assertTrue(self.error_message in data)
            self.assertTrue(self.fatal_message in data)

    def test_print_in_file_only_error_or_higher_levels(self):
        log = LogHelper()

        log.debug(self.debug_message)
        log.info(self.info_message)
        log.warning(self.warning_message)
        log.error(self.error_message)
        log.fatal(self.fatal_message)

        log_name = 'test_print_in_file_only_error_or_higher_levels.log'
        self.assertTrue(log.logs.__len__() == 5)
        self.assertEqual(log.save_logs(log_name, log_level=LogHelper.ERROR), True)
        with open(f'./{log_name}') as file:
            data = file.read()
            self.assertFalse(self.debug_message in data)
            self.assertFalse(self.info_message in data)
            self.assertFalse(self.warning_message in data)
            self.assertTrue(self.error_message in data)
            self.assertTrue(self.fatal_message in data)


if __name__ == '__main__':
    unittest.main()
