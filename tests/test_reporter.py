import unittest
from unittest.mock import MagicMock, patch
from src.reporter import SystemReporter

class TestReporter(unittest.TestCase):
    def setUp(self):
        self.reporter = SystemReporter()

    @patch('os.name', 'posix') # Test fallback
    def test_get_system_metrics(self):
        metrics = self.reporter.get_system_metrics()
        self.assertEqual(metrics['cpu_usage'], "N/A")
        
    @patch('shutil.disk_usage')
    def test_get_disk_usage(self, mock_disk):
        # total, used, free
        mock_disk.return_value = (500 * 1024 * 1024 * 1024, 250 * 1024 * 1024 * 1024, 250 * 1024 * 1024 * 1024)
        
        usage = self.reporter.get_disk_usage()
        self.assertEqual(usage['total'], "500.00 GB")
        self.assertEqual(usage['percent'], "50.0%")
        
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.path.exists')
    def test_find_large_files(self, mock_exists, mock_getsize, mock_walk):
        mock_exists.return_value = True
        mock_walk.return_value = [
            ('/root', [], ['bigfile.iso', 'smallfile.txt'])
        ]
        
        def getsize_side_effect(path):
            if 'bigfile.iso' in path:
                return 200 * 1024 * 1024 # 200MB
            return 1024 # 1KB
        
        mock_getsize.side_effect = getsize_side_effect
        
        large_files = self.reporter.find_large_files('/root')
        self.assertEqual(len(large_files), 1)
        self.assertEqual(large_files[0][0], '/root/bigfile.iso')
        self.assertEqual(large_files[0][1], '200.00 MB')

    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.path.exists')
    @patch('builtins.open')
    def test_find_duplicates(self, mock_open, mock_exists, mock_getsize, mock_walk):
        mock_exists.return_value = True
        mock_walk.return_value = [
            ('/root', [], ['file1.txt', 'file2.txt', 'file3.txt'])
        ]
        
        # All files same size
        mock_getsize.return_value = 100
        
        # Mocks for file read to simulate content
        # file1 and file3 are same content, file2 is different
        file_contents = {
            '/root/file1.txt': b'content_a',
            '/root/file2.txt': b'content_b',
            '/root/file3.txt': b'content_a'
        }
        
        # We need to correctly map open calls to return different contents
        # This is tricky with simple mocks, let's use a side effect for the file object
        class MockFile:
            def __init__(self, path):
                self.path = path
                self.data = file_contents[self.path]
                self.cursor = 0
            def __enter__(self):
                return self
            def __exit__(self, exc_type, exc_val, exc_tb):
                pass
            def read(self, size):
                if self.cursor >= len(self.data):
                    return b""
                chunk = self.data[self.cursor:self.cursor+size]
                self.cursor += len(chunk)
                return chunk

        def open_side_effect(file, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None):
             return MockFile(file)
             
        mock_open.side_effect = open_side_effect
        
        duplicates = self.reporter.find_duplicates('/root')
        
        # Should find 1 set of duplicates (size 100)
        self.assertEqual(len(duplicates), 1)
        self.assertEqual(duplicates[0][0], 100)
        self.assertEqual(len(duplicates[0][1]), 2)
        self.assertIn('/root/file1.txt', duplicates[0][1])
        self.assertIn('/root/file3.txt', duplicates[0][1])

if __name__ == '__main__':
    unittest.main()
