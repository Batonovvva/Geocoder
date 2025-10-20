import unittest
from unittest.mock import patch, MagicMock

import run_unittests


class TestRunUnittests(unittest.TestCase):
    @patch("unittest.TextTestRunner")
    @patch("unittest.TestLoader")
    @patch("sys.exit")
    def test_main_success_exit_zero(self, mock_exit, mock_loader_cls, mock_runner_cls):
        mock_suite = MagicMock()
        mock_loader = MagicMock()
        mock_loader.discover.return_value = mock_suite
        mock_loader_cls.return_value = mock_loader

        mock_result = MagicMock()
        mock_result.wasSuccessful.return_value = True
        mock_runner = MagicMock()
        mock_runner.run.return_value = mock_result
        mock_runner_cls.return_value = mock_runner

        run_unittests.main()
        mock_exit.assert_called_once_with(0)

    @patch("unittest.TextTestRunner")
    @patch("unittest.TestLoader")
    @patch("sys.exit")
    def test_main_failure_exit_one(self, mock_exit, mock_loader_cls, mock_runner_cls):
        mock_suite = MagicMock()
        mock_loader = MagicMock()
        mock_loader.discover.return_value = mock_suite
        mock_loader_cls.return_value = mock_loader

        mock_result = MagicMock()
        mock_result.wasSuccessful.return_value = False
        mock_runner = MagicMock()
        mock_runner.run.return_value = mock_result
        mock_runner_cls.return_value = mock_runner

        run_unittests.main()
        mock_exit.assert_called_once_with(1)


if __name__ == "__main__":
    unittest.main(verbosity=2)


