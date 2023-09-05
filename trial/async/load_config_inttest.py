import unittest
from load_config import load_config_async
import asyncio

class TestConfig(unittest.IsolatedAsyncioTestCase):

    async def test_database_host_exists(self):
        config_data = await load_config_async()

        # Check if 'database' key exists in the config_data dictionary
        self.assertIn('database', config_data)

        # Check if 'host' key exists within the 'database' dictionary
        db_config = config_data.get('database', {})
        self.assertIn('host', db_config)
        db_host = db_config.get('host')

        # Assert that db_host is not None
        self.assertIsNotNone(db_host)
        print(f"Database Host: {db_host}")

    # Add more test cases as needed for other configuration values

if __name__ == '__main__':
    unittest.main()
