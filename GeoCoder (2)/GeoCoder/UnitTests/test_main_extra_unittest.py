import unittest
from unittest.mock import patch, AsyncMock

import main


class TestMainCli(unittest.IsolatedAsyncioTestCase):
    @patch("sys.argv", ["main.py", "--examples"])
    @patch("builtins.print")
    async def test_examples_branch(self, mock_print):
        with self.assertRaises(SystemExit):
            await main.main()
        self.assertTrue(mock_print.called)

    @patch("sys.argv", ["main.py", "1"])
    @patch("main.parse.choose_input", new_callable=AsyncMock)
    async def test_choose_input_called(self, mock_choose_input):
        with self.assertRaises(SystemExit):
            await main.main()
        mock_choose_input.assert_awaited_once_with("1")

    @patch("sys.argv", ["main.py", "--badflag"])
    @patch("builtins.print")
    async def test_unknown_flag(self, mock_print):
        with self.assertRaises(SystemExit):
            await main.main()
        self.assertTrue(mock_print.called)


class TestEnsureDeps(unittest.TestCase):
    @patch("subprocess.check_call")
    def test_ensure_dependencies_installed(self, mock_check_call):
        main.ensure_dependencies_installed()
        self.assertTrue(mock_check_call.called)


if __name__ == "__main__":
    unittest.main(verbosity=2)


