import unittest
from unittest.mock import patch, AsyncMock, MagicMock

from Source.database.requests import add_new_address


class TestRequestsSuccess(unittest.IsolatedAsyncioTestCase):
    @patch("Source.database.requests.async_session")
    async def test_add_new_address_success(self, mock_async_session):
        mock_session = AsyncMock()
        mock_async_session.return_value.__aenter__.return_value = mock_session

        class _AsyncCM:
            async def __aenter__(self):
                return None

            async def __aexit__(self, exc_type, exc, tb):
                return False
            
        mock_session.begin = MagicMock(return_value=_AsyncCM())

        await add_new_address("q", "full", 1.0, 2.0)

        self.assertTrue(mock_session.add.called)


if __name__ == "__main__":
    unittest.main(verbosity=2)


