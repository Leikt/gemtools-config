import unittest
from unittest.mock import patch
from gemtoolsconfig.exceptions import critical


class TestCritical(unittest.TestCase):

    @patch('logging.critical')
    def test_critical_logs_message(self, mock_critical):
        message = 'This is a critical error'
        exception_class = Exception

        try:  # NOQA
            critical(message, exception_class)
        except:  # NOQA
            pass
        finally:
            mock_critical.assert_called_once_with(message)

    def test_critical_raises_exception(self):
        message = 'This is a critical error'
        exception_class = ValueError

        with self.assertRaises(ValueError):
            critical(message, exception_class)
