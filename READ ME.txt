## This is a program that performs one-way synchronization of two folders.
* Synchronization is carried out periodically and changes(file update, copying, removal operations) are displayed in the console and written to a log file.
* Folder paths, synchronization interval and log file path can be provided using command line arguments, but default values are set for testing purposes.



## Requirements

* Python 3.x
* Libraries: tqdm, os, time, shutil, argparse, logging



## Usage

```
python sync.py --source "C:\Users\TAWT\PySynch\sync" --destination "C:\Users\TAWT\PySynch\sync_copy" --log "C:\Users\TAWT\PySynch\sync_log.txt" --delete-extra --interval 10
```

## When to Use Quotation Marks

Path with Spaces: If any part of your file paths contains spaces (e.g., C:\My Documents\Folder), you must use quotes to prevent errors.
```
python sync.py --source "C:\My Documents\Folder\sync" --destination "C:\My Documents\Folder\sync_copy" --log "C:\My Documents\Folder\sync_log.txt" --delete-extra --interval 10
```

Path without Spaces: If your file paths do not contain spaces, you can omit the quotes:
```
python sync.py --source C:\Users\TAWT\PySynch\sync --destination C:\Users\TAWT\PySynch\sync_copy --log C:\Users\TAWT\PySynch\sync_log.txt --delete-extra --interval 10
```


## Notes

- If the replica folder does not exist, the script will create it.
- The script will raise an error if the source folder does not exist.
- The script will continuously monitor the source folder and synchronize it with the replica folder based on the specified time interval.
- Using the keyboard interrupt (CTRL+C) to stop the script manually.
