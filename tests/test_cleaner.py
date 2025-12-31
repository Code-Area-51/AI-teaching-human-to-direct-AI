import unittest
from unittest.mock import MagicMock, patch
import os
from src.cleaner import SystemCleaner

class TestCleaner(unittest.TestCase):
    def setUp(self):
        self.mock_action_handler = MagicMock()
        self.cleaner = SystemCleaner(self.mock_action_handler)

    @patch.dict(os.environ, {'TEMP': '/mock/temp', 'WINDIR': '/mock/windows', 'LOCALAPPDATA': '/mock/localappdata'})
    @patch('os.name', 'nt')
    def test_get_temp_paths(self):
        paths = self.cleaner.get_temp_paths()
        self.assertIn('/mock/temp', paths)
        self.assertIn('/mock/windows/Temp', paths)

    @patch.dict(os.environ, {'LOCALAPPDATA': '/mock/localappdata'})
    @patch('os.path.exists')
    @patch('os.listdir')
    def test_get_browser_cache_paths(self, mock_listdir, mock_exists):
        # Setup mocks
        mock_exists.return_value = True
        mock_listdir.return_value = ['profile1.default']
        
        paths = self.cleaner.get_browser_cache_paths()
        
        expected_chrome = os.path.join('/mock/localappdata', 'Google', 'Chrome', 'User Data', 'Default', 'Cache')
        expected_firefox = os.path.join('/mock/localappdata', 'Mozilla', 'Firefox', 'Profiles', 'profile1.default', 'cache2')
        
        self.assertIn(expected_chrome, paths)
        self.assertIn(expected_firefox, paths)

    @patch('os.path.exists')
    @patch('os.listdir')
    @patch('os.path.isfile')
    @patch('os.path.isdir')
    def test_clean_directory(self, mock_isdir, mock_isfile, mock_listdir, mock_exists):
        mock_exists.return_value = True
        mock_listdir.return_value = ['file1.txt', 'dir1']
        
        # Configure isfile/isdir
        # item_path will be constructed as /mock/path/file1.txt and /mock/path/dir1
        def isfile_side_effect(path):
            return path.endswith('file1.txt')
        def isdir_side_effect(path):
            return path.endswith('dir1')
            
        mock_isfile.side_effect = isfile_side_effect
        mock_isdir.side_effect = isdir_side_effect
        
        self.mock_action_handler.remove_file.return_value = 100 # size
        self.mock_action_handler.remove_dir.return_value = True

        count, size = self.cleaner.clean_directory('/mock/path')
        
        self.assertEqual(count, 2)
        self.assertEqual(size, 100)
        self.mock_action_handler.remove_file.assert_called_once()
        self.mock_action_handler.remove_dir.assert_called_once()

if __name__ == '__main__':
    unittest.main()
