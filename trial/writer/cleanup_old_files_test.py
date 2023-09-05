import unittest
import os
from pathlib import Path
from datetime import datetime, timedelta
from tempfile import TemporaryDirectory
from cleanup_old_files import cleanup_old_files

class TestCleanupOldFiles(unittest.TestCase):
    def test_cleanup_with_timestamps(self):
        # Create a temporary directory for testing
        with TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)

            # Create some test files with filenames containing timestamps
            today = datetime.now()
            old_date = today - timedelta(days=2)
            older_date = today - timedelta(days=3)

            file1_name = f'file1_{old_date.strftime("%Y%m%d%H%M%S")}.txt'
            file2_name = f'file2_{today.strftime("%Y%m%d%H%M%S")}.txt'
            file3_name = f'file3_{older_date.strftime("%Y%m%d%H%M%S")}.txt'

            file1_path = temp_dir_path / file1_name
            file2_path = temp_dir_path / file2_name
            file3_path = temp_dir_path / file3_name

            file1_path.touch()
            file2_path.touch()
            file3_path.touch()

            # Call the cleanup function with a threshold of 1 day
            cleanup_old_files(temp_dir_path, days_threshold=1)

            # Verify that only file2 should remain (newer than 1 day)
            self.assertTrue(file1_path.exists())
            self.assertFalse(file2_path.exists())
            self.assertFalse(file3_path.exists())

if __name__ == '__main__':
    unittest.main()
