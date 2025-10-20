import unittest
from unittest.mock import patch, AsyncMock, MagicMock

from Source.response import send_request


class TestResponse(unittest.IsolatedAsyncioTestCase):
    @patch("Source.response.return_address_if_exist", new_callable=AsyncMock)
    @patch("Source.response.parse.parse_output_address", new_callable=AsyncMock)
    @patch("Source.response.requests.get")
    async def test_successful_request_processing(self, mock_http_get, mock_output_parser, mock_cache_check):
        mock_cache_check.return_value = None

        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.json.return_value = [{
            "display_name": "Екатеринбург, Россия",
            "lat": "56.8389",
            "lon": "60.6057",
        }]
        mock_http_get.return_value = mock_response

        await send_request("Екатеринбург")

        mock_output_parser.assert_awaited_once()

    @patch("Source.response.return_address_if_exist", new_callable=AsyncMock)
    @patch("Source.response.requests.get")
    async def test_empty_response_handling(self, mock_http_get, mock_cache_check):
        mock_cache_check.return_value = None

        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.json.return_value = []
        mock_http_get.return_value = mock_response

        with patch("builtins.print") as mock_print:
            await send_request("несуществующий адрес")

        self.assertTrue(mock_print.called)

    @patch("Source.response.return_address_if_exist", new_callable=AsyncMock)
    @patch("Source.response.requests.get")
    async def test_http_error_handling(self, mock_http_get, mock_cache_check):
        mock_cache_check.return_value = None

        mock_response = MagicMock()
        mock_response.ok = False
        mock_response.status_code = 500
        mock_http_get.return_value = mock_response

        with patch("builtins.print") as mock_print:
            await send_request("адрес с ошибкой")

        printed_messages = [call[0][0] for call in mock_print.call_args_list]
        self.assertTrue(any("Ошибка HTTP: 500" in str(msg) for msg in printed_messages))

    @patch("Source.response.return_address_if_exist", new_callable=AsyncMock)
    @patch("Source.response.requests.get")
    async def test_network_exception_handling(self, mock_http_get, mock_cache_check):
        mock_cache_check.return_value = None
        mock_http_get.side_effect = Exception("таймаут соединения")

        with patch("builtins.print") as mock_print:
            await send_request("проблемный адрес")

        error_messages = [call[0][0] for call in mock_print.call_args_list]
        self.assertTrue(any("Ошибка запроса" in str(msg) for msg in error_messages))

    @patch("Source.response.return_address_if_exist", new_callable=AsyncMock)
    async def test_cached_data_retrieval(self, mock_cache_check):
        mock_cached_address = MagicMock()
        mock_cached_address.latitude = "56.8389"
        mock_cached_address.longitude = "60.6057"
        mock_cached_address.full_address = "Екатеринбург, Россия"
        mock_cache_check.return_value = mock_cached_address

        with patch("builtins.print") as mock_print:
            await send_request("Екатеринбург")

        printed_output = [call[0][0] for call in mock_print.call_args_list]
        # Cached branch prints only the full address
        self.assertTrue(any("Полный адрес: Екатеринбург, Россия" in str(msg) for msg in printed_output))

    @patch("Source.response.return_address_if_exist", new_callable=AsyncMock)
    @patch("Source.response.requests.get")
    async def test_malformed_response_handling(self, mock_http_get, mock_cache_check):
        mock_cache_check.return_value = None

        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.json.return_value = [{"invalid": "data"}]
        mock_http_get.return_value = mock_response

        with patch("builtins.print") as mock_print:
            await send_request("адрес с некорректным ответом")

        self.assertTrue(mock_print.called)

    @patch("Source.response.return_address_if_exist", new_callable=AsyncMock)
    async def test_cache_miss_behavior(self, mock_cache_check):
        mock_cache_check.return_value = None

        with patch("Source.response.requests.get") as mock_http_get, \
             patch("Source.response.parse.parse_output_address", new_callable=AsyncMock):
            mock_response = MagicMock()
            mock_response.ok = True
            mock_response.json.return_value = [{
                "display_name": "Тестовый адрес",
                "lat": "55.7558",
                "lon": "37.6173",
            }]
            mock_http_get.return_value = mock_response

            await send_request("новый адрес")

            self.assertTrue(mock_http_get.called)


if __name__ == "__main__":
    unittest.main(verbosity=2)


