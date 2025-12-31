import os
from src.utils import logger

class FileOrganizer:
    EXTENSIONS = {
        'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'],
        'Documents': ['.pdf', '.docx', '.doc', '.txt', '.xlsx', '.xls', '.pptx', '.ppt', '.csv', '.rtf'],
        'Installers': ['.exe', '.msi', '.iso', '.dmg', '.pkg', '.deb', '.rpm'],
        'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz'],
        'Audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a'],
        'Video': ['.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm'],
        'Misc': []  # Catch-all
    }

    def __init__(self, action_handler):
        self.action = action_handler

    def get_category(self, filename):
        """Determines the category of a file based on its extension."""
        _, ext = os.path.splitext(filename)
        ext = ext.lower()
        
        for category, extensions in self.EXTENSIONS.items():
            if ext in extensions:
                return category
        return 'Misc'

    def organize_directory(self, dirpath):
        """Organizes files in the specified directory into subfolders."""
        if not dirpath or not os.path.exists(dirpath):
            logger.warning(f"Directory not found, skipping organization: {dirpath}")
            return 0

        logger.info(f"Organizing directory: {dirpath}")
        count = 0
        
        try:
            for item in os.listdir(dirpath):
                src_path = os.path.join(dirpath, item)
                
                # Skip directories (don't move folders inside folders recursively in this version)
                if not os.path.isfile(src_path):
                    continue
                    
                category = self.get_category(item)
                
                # If Misc and it's not a hidden file or system file, maybe skip?
                # User asked to group Misc as well.
                # However, we should be careful not to move 'desktop.ini' or similar if organizing desktop.
                if item.lower() in ['desktop.ini', 'thumbs.db']:
                    continue
                
                # Skip shortcuts and URL files to preserve Desktop icons
                if item.lower().endswith(('.lnk', '.url')):
                    continue

                dest_dir = os.path.join(dirpath, category)
                
                # Ensure destination directory exists
                if self.action.create_dir(dest_dir):
                    dest_path = os.path.join(dest_dir, item)
                    # Move file
                    if self.action.move_file(src_path, dest_path):
                        count += 1
                        
        except Exception as e:
            logger.error(f"Error organizing directory {dirpath}: {e}")
            
        logger.info(f"Organization complete. Moved {count} files in {dirpath}.")
        return count

    def run(self):
        """Executes the organization process for Desktop and Downloads."""
        total_moved = 0
        
        paths = []
        if os.name == 'nt':
            user_profile = os.environ.get('USERPROFILE')
            if user_profile:
                paths.append(os.path.join(user_profile, 'Desktop'))
                paths.append(os.path.join(user_profile, 'Downloads'))
        
        for path in paths:
            total_moved += self.organize_directory(path)
            
        return total_moved
