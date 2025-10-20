import unittest
from unittest.mock import AsyncMock, patch

from Source.parsing import parse_output_address


class TestParsingExtra(unittest.IsolatedAsyncioTestCase):
    async def test_missing_lat_lon(self):
        bad = {"display_name": "Адрес, Россия", "address": {"country": "Россия"}}
        await parse_output_address("q", bad)

    async def test_country_field_not_russia(self):
        foreign = {
            "display_name": "Something, USA",
            "lat": "1",
            "lon": "2",
            "address": {"country": "США"},
        }
        await parse_output_address("q", foreign)

    async def test_no_country_checks_display_name_suffix(self):
        data = {
            "display_name": "Город, Регион, Россия",
            "lat": "1",
            "lon": "2",
            "address": {},
        }
        with patch("Source.parsing.add_new_address", new_callable=AsyncMock) as mock_add:
            await parse_output_address("q", data)
            mock_add.assert_awaited_once()


if __name__ == "__main__":
    unittest.main(verbosity=2)


