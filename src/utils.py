import logging
import os
import shutil

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def format_size(size_bytes):
    """Format file size from bytes to human readable string."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"

class ActionHandler:
    """
    Handles file operations with support for Dry Run mode.
    """
    def __init__(self, dry_run=True):
        self.dry_run = dry_run

    def remove_file(self, filepath):
        """Removes a file safely. Returns the size of the file removed."""
        try:
            size = 0
            if os.path.exists(filepath):
                size = os.path.getsize(filepath)

            if self.dry_run:
                logger.info(f"[DRY RUN] Would delete file: {filepath} ({format_size(size)})")
                return size
            else:
                os.remove(filepath)
                logger.info(f"Deleted file: {filepath} ({format_size(size)})")
                return size
        except Exception as e:
            logger.error(f"Error deleting {filepath}: {e}")
            return 0

    def remove_dir(self, dirpath):
        """Removes a directory recursively."""
        try:
            if self.dry_run:
                logger.info(f"[DRY RUN] Would delete directory: {dirpath}")
                return True
            else:
                shutil.rmtree(dirpath)
                logger.info(f"Deleted directory: {dirpath}")
                return True
        except Exception as e:
            logger.error(f"Error deleting directory {dirpath}: {e}")
            return False

    def move_file(self, src, dest):
        """Moves a file."""
        try:
            if self.dry_run:
                logger.info(f"[DRY RUN] Would move {src} to {dest}")
                return True
            else:
                shutil.move(src, dest)
                logger.info(f"Moved {src} to {dest}")
                return True
        except Exception as e:
            logger.error(f"Error moving {src} to {dest}: {e}")
            return False

    def create_dir(self, dirpath):
        """Creates a directory if it doesn't exist."""
        try:
            if os.path.exists(dirpath):
                return True
                
            if self.dry_run:
                logger.info(f"[DRY RUN] Would create directory: {dirpath}")
                return True
            else:
                os.makedirs(dirpath)
                logger.info(f"Created directory: {dirpath}")
                return True
        except Exception as e:
            logger.error(f"Error creating directory {dirpath}: {e}")
            return False
