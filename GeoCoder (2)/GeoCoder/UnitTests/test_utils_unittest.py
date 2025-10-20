import unittest

from Source.utils import build_address_from_components


class TestUtilsAddressBuilder(unittest.TestCase):
    def test_full_components(self):
        address = {
            "house_number": "7",
            "road": "Родонитовая улица",
            "city": "Екатеринбург",
            "state": "Свердловская область",
            "postcode": "620089",
            "country": "Россия",
        }
        result = build_address_from_components(address)
        self.assertEqual(
            result,
            "7 Родонитовая улица; Екатеринбург; Свердловская область; 620089; Россия",
        )

    def test_only_road_and_city(self):
        address = {
            "road": "Родонитовая улица",
            "city": "Екатеринбург",
        }
        result = build_address_from_components(address)
        self.assertEqual(result, "Родонитовая улица; Екатеринбург")

    def test_no_data_returns_none(self):
        self.assertIsNone(build_address_from_components({}))

    def test_missing_country(self):
        address = {
            "house": "1",
            "street": "Ленина",
            "town": "Пермь",
        }
        result = build_address_from_components(address)
        self.assertEqual(result, "1 Ленина; Пермь")


if __name__ == "__main__":
    unittest.main(verbosity=2)


