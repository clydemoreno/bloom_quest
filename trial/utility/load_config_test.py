import unittest
from load_config import load_config

class TestLoadConfig(unittest.TestCase):
    def test_load_config(self):
        # Load the config
        config = load_config()

        # Assert that the loaded config has the expected structure
        self.assertIsInstance(config, dict)
        self.assertIn("database", config)
        self.assertIn("data", config)
        self.assertIn("bloom_filter", config)

if __name__ == '__main__':
    unittest.main()
