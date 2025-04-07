import os
import time
import logging
from pathlib import Path
from config import Config

class PDFCacheCleaner:
    @staticmethod
    def get_directory_size(path):
        """calculate the total size of a directory"""
        total = 0
        for dirpath, _, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if os.path.exists(fp):
                    total += os.path.getsize(fp)
        return total

    @staticmethod
    def find_oldest_files(path, extension=".pdf"):
        """sort files by modification time"""
        file_list = []
        for root, _, files in os.walk(path):
            for file in files:
                if file.lower().endswith(extension):
                    file_path = os.path.join(root, file)
                    stat = os.stat(file_path)
                    file_list.append({
                        "path": file_path,
                        "mtime": stat.st_mtime,
                        "size": stat.st_size
                    })
        
        return sorted(file_list, key=lambda x: x["mtime"])

    @classmethod
    def cleanup_pdfs(cls):
        """cache cleaner"""
        base_path = Path(Config.BASE_PATH)
        if not base_path.exists():
            logging.warning(f"Base path {base_path} does not exist, skipping cleanup")
            return

        # calculate total size
        total_bytes = cls.get_directory_size(base_path)
        max_bytes = Config.MAX_STORAGE_GB * 1024**3
        threshold = max_bytes * Config.CLEANUP_THRESHOLD

        if total_bytes < threshold:
            logging.info(f"Current size: {total_bytes/1024**3:.2f} GB < Threshold {threshold/1024**3:.2f} GB, not need to cleanup")
            return

        # obtain the oldest files
        files = cls.find_oldest_files(base_path)
        removed = 0
        removed_size = 0

        # delete files until the size is below the threshold
        while total_bytes > threshold and files:
            target = files.pop(0)
            try:
                os.remove(target["path"])
                total_bytes -= target["size"]
                removed += 1
                removed_size += target["size"]
                
                # record the deletion
                logging.info(f"Delete old file: {target['path']} "
                            f"({time.ctime(target['mtime'])}, {target['size']/1024**2:.2f}MB)")
                
                # optional: remove empty directories
                parent_dir = os.path.dirname(target["path"])
                if not os.listdir(parent_dir):
                    os.rmdir(parent_dir)
                    logging.info(f"Delete empty directory: {parent_dir}")
                    
            except Exception as e:
                logging.error(f"Fail to delete file: {target['path']} - {str(e)}")

        logging.info(f"Deletion completed: deleted {removed} files, released {removed_size/1024**3:.2f} GB")

if __name__ == '__main__':
    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Run the PDF cache cleaner
    PDFCacheCleaner.cleanup_pdfs()
    logging.info("PDF cache cleaner finished.")

