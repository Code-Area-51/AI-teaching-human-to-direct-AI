import unittest
from src.utils import format_size, ActionHandler
import os

class TestUtils(unittest.TestCase):
    def test_format_size(self):
        self.assertEqual(format_size(100), "100.00 B")
        self.assertEqual(format_size(1024), "1.00 KB")
        self.assertEqual(format_size(1024 * 1024), "1.00 MB")
        self.assertEqual(format_size(1024 * 1024 * 1024), "1.00 GB")

    def test_action_handler_dry_run(self):
        handler = ActionHandler(dry_run=True)
        # In dry run, it should just log and return True, not actually do anything.
        # remove_file returns size (0 if not exists)
        self.assertEqual(handler.remove_file("/tmp/nonexistent_file_xyz"), 0)
        self.assertTrue(handler.move_file("/tmp/src", "/tmp/dest"))

if __name__ == '__main__':
    unittest.main()
