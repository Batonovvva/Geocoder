import unittest
from unittest.mock import patch, AsyncMock

import main


class TestHelpAndCommands(unittest.TestCase):
    @patch("builtins.print")
    def test_show_help(self, mock_print):
        main.show_help()
        self.assertTrue(mock_print.called)


class TestCommandProcessing(unittest.IsolatedAsyncioTestCase):
    @patch("main.parse.choose_input", new_callable=AsyncMock)
    async def test_process_command_choose_input(self, mock_choose_input):
        await main.process_command("1")
        mock_choose_input.assert_awaited_once_with("1")

        mock_choose_input.reset_mock()
        await main.process_command("2")
        mock_choose_input.assert_awaited_once_with("2")

    @patch("builtins.print")
    async def test_process_command_help(self, mock_print):
        await main.process_command("--help")
        self.assertTrue(mock_print.called)

        mock_print.reset_mock()
        await main.process_command("-h")
        self.assertTrue(mock_print.called)

    @patch("builtins.print")
    async def test_process_command_unknown(self, mock_print):
        await main.process_command("unknown_command")
        mock_print.assert_called_with("Неизвестная команда. Введите --help для справки.")

    @patch("sys.exit")
    @patch("builtins.print")
    async def test_process_command_exit(self, mock_print, mock_exit):
        await main.process_command("exit")
        mock_exit.assert_called_once_with(0)
        mock_print.assert_called_with("Выход из программы.")

    @patch("main.process_command", new_callable=AsyncMock)
    @patch("builtins.input", side_effect=["exit"])
    async def test_interactive_mode_exit(self, mock_input, mock_process_command):
        mock_process_command.side_effect = SystemExit(0)
        with self.assertRaises(SystemExit):
            await main.interactive_mode()
        mock_process_command.assert_awaited_once_with("exit")


if __name__ == "__main__":
    unittest.main(verbosity=2)


