import unittest
from unittest.mock import patch, AsyncMock

from Source.parsing import (
    clean_address,
    build_normalized_address,
    sanitize_input,
    parse_input_address,
    parse_input_coordinates,
    parse_output_address,
    choose_input,
)


MOCK_CLEANED_ADDRESS = {
    "street": "Родонитовая",
    "house": "7",
    "city": "Екатеринбург",
    "region": "Свердловская",
    "country": "Россия",
}

MOCK_OUTPUT_ADDRESS = {
    "display_name": "Родонитовая 7, Екатеринбург, Свердловская, Россия",
    "lat": "56.8389",
    "lon": "60.6057",
}


class TestAddressProcessing(unittest.TestCase):
    @patch("Source.parsing.dadata.clean")
    def test_successful_address_cleaning(self, mock_dadata_clean):
        mock_dadata_clean.return_value = MOCK_CLEANED_ADDRESS
        processed_address = clean_address("Родонитовая 7 Екатеринбург Россия")
        self.assertEqual(processed_address, MOCK_CLEANED_ADDRESS)

    @patch("Source.parsing.dadata.clean", side_effect=Exception("Ошибка Dadata"))
    def test_failed_address_cleaning(self, mock_dadata_clean):
        processed_address = clean_address("Некорректный адрес")
        self.assertIsNone(processed_address)

    def test_complete_address_normalization(self):
        normalized = build_normalized_address(MOCK_CLEANED_ADDRESS)
        expected_result = "Родонитовая 7 Екатеринбург Свердловская Россия"
        self.assertEqual(normalized, expected_result)

    def test_empty_data_normalization(self):
        self.assertIsNone(build_normalized_address({}))


class TestUserInputProcessing(unittest.IsolatedAsyncioTestCase):
    @patch("builtins.input", side_effect=["екатеринбург", "родонитовая", "7"])
    @patch("Source.parsing.clean_address", return_value=MOCK_CLEANED_ADDRESS)
    @patch("Source.parsing.build_normalized_address", return_value="Родонитовая 7 Екатеринбург Свердловская Россия")
    @patch("Source.parsing.req.send_request", new_callable=AsyncMock)
    async def test_successful_address_parsing(self, mock_send_request, mock_build_address, mock_clean_address, mock_user_input):
        await parse_input_address()
        mock_send_request.assert_awaited_once()

    @patch("builtins.input", side_effect=["екатеринбург", "родонитовая", "7"])
    @patch("Source.parsing.clean_address", return_value=None)
    async def test_failed_address_parsing(self, mock_clean_address, mock_user_input):
        await parse_input_address()

    @patch("builtins.input", return_value="56.8389 60.6057")
    @patch("Source.parsing.req.send_request", new_callable=AsyncMock)
    async def test_successful_coordinate_parsing(self, mock_send_request, mock_user_input):
        await parse_input_coordinates()
        mock_send_request.assert_awaited_once_with("56.8389 60.6057")

    @patch("builtins.input", return_value="abc def")
    async def test_invalid_coordinate_parsing(self, mock_user_input):
        await parse_input_coordinates()


class TestOutputProcessing(unittest.IsolatedAsyncioTestCase):
    async def test_successful_output_processing(self):
        with patch("Source.parsing.add_new_address", new_callable=AsyncMock) as mock_add_address:
            await parse_output_address("Родонитовая 7 Екатеринбург", MOCK_OUTPUT_ADDRESS)
            mock_add_address.assert_awaited_once()

    async def test_empty_output_processing(self):
        await parse_output_address("Родонитовая 7 Екатеринбург", {})

    async def test_non_russian_address_processing(self):
        foreign_address = MOCK_OUTPUT_ADDRESS.copy()
        foreign_address["display_name"] = "Somewhere Else"
        await parse_output_address("address", foreign_address)


class TestInputSelection(unittest.IsolatedAsyncioTestCase):
    @patch("Source.parsing.parse_input_address", new_callable=AsyncMock)
    @patch("Source.parsing.parse_input_coordinates", new_callable=AsyncMock)
    async def test_input_type_selection(self, mock_process_coordinates, mock_process_address):
        await choose_input("1")
        mock_process_coordinates.assert_awaited_once()

        await choose_input("2")
        mock_process_address.assert_awaited_once()

    async def test_invalid_input_selection(self):
        await choose_input("3")


class TestInputSanitization(unittest.TestCase):
    def test_text_sanitization_processing(self):
        self.assertEqual(sanitize_input("  Екатеринбург "), "екатеринбург")
        self.assertIsNone(sanitize_input("   "))


if __name__ == "__main__":
    unittest.main(verbosity=2)


