import unittest
from unittest.mock import MagicMock, patch
import os
from src.organizer import FileOrganizer

class TestOrganizer(unittest.TestCase):
    def setUp(self):
        self.mock_action_handler = MagicMock()
        self.organizer = FileOrganizer(self.mock_action_handler)

    def test_get_category(self):
        self.assertEqual(self.organizer.get_category('photo.jpg'), 'Images')
        self.assertEqual(self.organizer.get_category('document.pdf'), 'Documents')
        self.assertEqual(self.organizer.get_category('installer.exe'), 'Installers')
        self.assertEqual(self.organizer.get_category('archive.zip'), 'Archives')
        self.assertEqual(self.organizer.get_category('song.mp3'), 'Audio')
        self.assertEqual(self.organizer.get_category('movie.mp4'), 'Video')
        self.assertEqual(self.organizer.get_category('unknown.xyz'), 'Misc')

    @patch('os.path.exists')
    @patch('os.listdir')
    @patch('os.path.isfile')
    def test_organize_directory(self, mock_isfile, mock_listdir, mock_exists):
        mock_exists.return_value = True
        mock_listdir.return_value = ['photo.jpg', 'doc.pdf', 'folder']
        
        # Setup isfile to distinguish file from folder
        def isfile_side_effect(path):
            return not path.endswith('folder')
        mock_isfile.side_effect = isfile_side_effect
        
        self.mock_action_handler.create_dir.return_value = True
        self.mock_action_handler.move_file.return_value = True

        count = self.organizer.organize_directory('/mock/downloads')
        
        self.assertEqual(count, 2) # Only photo.jpg and doc.pdf should be moved
        
        # Verify create_dir called for Images and Documents
        self.mock_action_handler.create_dir.assert_any_call(os.path.join('/mock/downloads', 'Images'))
        self.mock_action_handler.create_dir.assert_any_call(os.path.join('/mock/downloads', 'Documents'))
        
        # Verify move_file calls
        self.mock_action_handler.move_file.assert_any_call(
            os.path.join('/mock/downloads', 'photo.jpg'),
            os.path.join('/mock/downloads', 'Images', 'photo.jpg')
        )

if __name__ == '__main__':
    unittest.main()
