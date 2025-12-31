import os
import glob
from src.utils import logger

class SystemCleaner:
    def __init__(self, action_handler):
        self.action = action_handler

    def get_temp_paths(self):
        """Returns a list of common Windows temporary file paths."""
        paths = []
        # Using environment variables to be safe and dynamic
        # These will be mocked in tests
        if 'TEMP' in os.environ:
            paths.append(os.environ['TEMP'])
        
        # Windows Directory Temp
        if 'WINDIR' in os.environ:
            paths.append(os.path.join(os.environ['WINDIR'], 'Temp'))
            
        return [p for p in paths if p]

    def get_browser_cache_paths(self):
        """Returns a list of browser cache paths."""
        paths = []
        local_app_data = os.environ.get('LOCALAPPDATA')
        
        if local_app_data:
            # Chrome
            paths.append(os.path.join(local_app_data, 'Google', 'Chrome', 'User Data', 'Default', 'Cache'))
            # Edge
            paths.append(os.path.join(local_app_data, 'Microsoft', 'Edge', 'User Data', 'Default', 'Cache'))
            # Firefox
            firefox_profiles = os.path.join(local_app_data, 'Mozilla', 'Firefox', 'Profiles')
            if os.path.exists(firefox_profiles):
                for profile in os.listdir(firefox_profiles):
                    paths.append(os.path.join(firefox_profiles, profile, 'cache2'))
        return paths

    def clean_directory(self, dirpath):
        """Removes all files and subdirectories in a directory. Returns (count, size_bytes)."""
        if not dirpath or not os.path.exists(dirpath):
            logger.warning(f"Directory not found, skipping: {dirpath}")
            return 0, 0
        
        logger.info(f"Cleaning directory: {dirpath}")
        count = 0
        total_size = 0
        try:
            for item in os.listdir(dirpath):
                item_path = os.path.join(dirpath, item)
                if os.path.isfile(item_path):
                    size = self.action.remove_file(item_path)
                    # We assume successful removal if no exception was raised in remove_file (it returns >=0)
                    count += 1
                    total_size += size
                elif os.path.isdir(item_path):
                    if self.action.remove_dir(item_path):
                        count += 1
                        # remove_dir doesn't calculate size recursively yet.
                        # For simplicity, we only count file sizes in this iteration.
        except Exception as e:
            logger.error(f"Error accessing directory {dirpath}: {e}")
        
        return count, total_size

    def run(self):
        """Executes the cleaning process. Returns (count, total_bytes_freed)."""
        total_cleaned = 0
        total_bytes = 0
        
        # Clean Temp Files
        for temp_path in self.get_temp_paths():
            c, s = self.clean_directory(temp_path)
            total_cleaned += c
            total_bytes += s

        # Clean Browser Caches
        for cache_path in self.get_browser_cache_paths():
            c, s = self.clean_directory(cache_path)
            total_cleaned += c
            total_bytes += s

        return total_cleaned, total_bytes
