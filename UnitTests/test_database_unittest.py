import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from Source.database.requests import return_address_if_exist, add_new_address


class TestDatabase(unittest.IsolatedAsyncioTestCase):
    @patch("Source.database.requests.async_session")
    async def test_return_address_if_exist_found(self, mock_async_session):
        mock_result = AsyncMock()
        mock_result.scalar_one_or_none = MagicMock(return_value="address_obj")

        mock_session = AsyncMock()
        mock_session.execute = AsyncMock(return_value=mock_result)

        mock_async_session.return_value.__aenter__.return_value = mock_session

        result = await return_address_if_exist("test query")
        self.assertEqual(result, "address_obj")
        mock_session.execute.assert_awaited()

    @patch("Source.database.requests.async_session")
    async def test_return_address_if_exist_not_found(self, mock_async_session):
        mock_result = AsyncMock()
        mock_result.scalar_one_or_none = MagicMock(return_value=None)

        mock_session = AsyncMock()
        mock_session.execute = AsyncMock(return_value=mock_result)

        mock_async_session.return_value.__aenter__.return_value = mock_session

        result = await return_address_if_exist("missing query")
        self.assertIsNone(result)

    @patch("Source.database.requests.async_session")
    async def test_add_new_address_exception(self, mock_async_session):
        mock_session = AsyncMock()
        mock_session.begin.return_value.__aenter__.side_effect = Exception("DB error")
        mock_async_session.return_value.__aenter__.return_value = mock_session

        with self.assertRaises(Exception):
            await add_new_address(
                input_query="failing query",
                full_address="fail address",
                lat=0.0,
                lon=0.0
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)


