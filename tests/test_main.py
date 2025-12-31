import unittest
from unittest.mock import patch, MagicMock
import sys
from io import StringIO
from assistant import main

class TestAssistant(unittest.TestCase):
    
    @patch('assistant.SystemCleaner')
    @patch('assistant.FileOrganizer')
    @patch('assistant.SystemReporter')
    def test_main_clean(self, mock_reporter, mock_organizer, mock_cleaner):
        # Mock run to return tuple
        mock_cleaner.return_value.run.return_value = (5, 1024)
        
        test_args = ['assistant.py', '--clean']
        with patch.object(sys, 'argv', test_args):
            main()
            mock_cleaner.return_value.run.assert_called_once()
            mock_organizer.return_value.run.assert_not_called()
            mock_reporter.return_value.generate_report.assert_not_called()

    @patch('assistant.SystemCleaner')
    @patch('assistant.FileOrganizer')
    @patch('assistant.SystemReporter')
    def test_main_organize(self, mock_reporter, mock_organizer, mock_cleaner):
        test_args = ['assistant.py', '--organize']
        with patch.object(sys, 'argv', test_args):
            main()
            mock_cleaner.return_value.run.assert_not_called()
            mock_organizer.return_value.run.assert_called_once()
            mock_reporter.return_value.generate_report.assert_not_called()

    @patch('assistant.SystemCleaner')
    @patch('assistant.FileOrganizer')
    @patch('assistant.SystemReporter')
    def test_main_report(self, mock_reporter, mock_organizer, mock_cleaner):
        test_args = ['assistant.py', '--report']
        with patch.object(sys, 'argv', test_args):
            main()
            mock_reporter.return_value.generate_report.assert_called_once()

    @patch('assistant.ActionHandler')
    @patch('assistant.SystemCleaner')
    def test_dry_run_flag(self, mock_cleaner, mock_action_handler):
        # Mock run to return tuple to avoid unpack error in assistant.py
        mock_cleaner.return_value.run.return_value = (0, 0)
        
        # Default is dry-run = True
        test_args = ['assistant.py', '--clean']
        with patch.object(sys, 'argv', test_args):
            main()
            mock_action_handler.assert_called_with(dry_run=True)
            
        # Explicit dry-run
        test_args = ['assistant.py', '--clean', '--dry-run']
        with patch.object(sys, 'argv', test_args):
            main()
            mock_action_handler.assert_called_with(dry_run=True)

        # No dry run
        test_args = ['assistant.py', '--clean', '--no-dry-run']
        with patch.object(sys, 'argv', test_args):
            main()
            mock_action_handler.assert_called_with(dry_run=False)

if __name__ == '__main__':
    unittest.main()
