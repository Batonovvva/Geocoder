import unittest
from unittest.mock import patch, AsyncMock

from Source.database import models


class TestModelsInitDb(unittest.IsolatedAsyncioTestCase):
    @patch("Source.database.models.engine")
    async def test_init_db_calls_create_all(self, mock_engine):
        mock_conn_cm = AsyncMock()
        mock_engine.begin.return_value = mock_conn_cm
        await models.init_db()
        self.assertTrue(mock_conn_cm.__aenter__.return_value.run_sync.called)


if __name__ == "__main__":
    unittest.main(verbosity=2)


