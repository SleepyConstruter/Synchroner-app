import os
import shutil
from tqdm import tqdm  # Import tqdm for the progress bar
import time
import logging
import argparse


def setup_logger(log_file= "sync_log.text"):
    
    logger = logging.getLogger("SyncLogger")
    logger.setLevel(logging.INFO)
        # Create file handler to log to a file
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)

    # Create console handler to log to the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Define log format
    log_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(log_format)
    console_handler.setFormatter(log_format)

    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

def sync_folders_with_progress_updates(source, destination, logger, delete_extra=False, update_interval=20):
    """
    Synchronize files and folders from the source to the destination with a progress bar.
    """
    # Ensure source exists
    if not os.path.exists(source):
        logger.error(f"Source folder '{source}' does not exist!")
        return

    # Create destination if it doesn't exist
    if not os.path.exists(destination):
        os.makedirs(destination)
        logger.info(f"Created destination folder: {destination}")

    # Collect all files to sync
    files_to_copy = []
    source_file_set = set()
    
    for root, _, files in os.walk(source):
        for file in files:
            source_file = os.path.join(root, file)
            relative_path = os.path.relpath(root, source)
            destination_file = os.path.join(destination, relative_path, file)
            files_to_copy.append((source_file, destination_file))
            source_file_set.add(destination_file)
                        
    total_files = len(files_to_copy)
    logger.info(f"Found {total_files} files to synchronize.")
    
    # Initialize tqdm progress bar
    progress_bar = tqdm(total=total_files, desc="Syncing Files", unit="file")

    # Use tqdm to show progress
    for i, (source_file, dest_file) in enumerate(files_to_copy, start=1):
        dest_dir = os.path.dirname(dest_file)

        # Create destination directory if it doesn't exist
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
            logger.info(f"Created directory: {dest_dir}")

        # Copy file if it doesn't exist or is outdated
        if not os.path.exists(dest_file) or os.path.getmtime(source_file) > os.path.getmtime(dest_file):
            shutil.copy2(source_file, dest_file)
            logger.info(f"Copied: {source_file} -> {dest_file}")
            
        time.sleep(0.1)
            
         # Update progress bar periodically
        if i % update_interval == 0 or i == total_files:  # Update on every `update_interval` or final file
            progress_bar.n = i
            progress_bar.refresh()
            
    progress_bar.close()
    # Optional: Remove files in destination that are not in the source
    if delete_extra:
        for root, _, files in os.walk(destination):
            for file in files:
                dest_file = os.path.join(root, file)
                if dest_file not in source_file_set:
                    os.remove(dest_file)
                    logger.info(f"Removed: {dest_file}")
                      
    logger.info("Sync complete!")

if __name__ == "__main__":
    try:
        # Parse command-line arguments
        parser = argparse.ArgumentParser(description="Synchronize folders with logging.")
        parser.add_argument("--source", required=True, help="Path to the source directory.")
        parser.add_argument("--destination", required=True, help="Path to the destination directory.")
        parser.add_argument("--log", required=True, help="Path to the log file.")
        parser.add_argument("--delete-extra", action="store_true", help="Delete extra files in the destination not present in the source.")
        parser.add_argument("--interval", type=int, default=10, help="Progress update interval.")
    
        args = parser.parse_args()
    
    
    #Example paths  hard coding:
    
    #source_folder = r"C:\Users\TAWT\PySynch\sync"
    #destination_folder = r"C:\Users\TAWT\PySynch\sync_copy"
        
    
        logger = setup_logger(args.log)

    # Run the sync function
        sync_folders_with_progress_updates(source=args.source, destination=args.destination, logger=logger, delete_extra=args.delete_extra, update_interval=args.interval)
    
    except KeyboardInterrupt:
        print("\nProcess interrupted by user.")
        logger.info("Process interrupted by user.")
        
        