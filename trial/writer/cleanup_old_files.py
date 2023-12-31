import os
from pathlib import Path
from datetime import datetime, timedelta

def cleanup_old_files(directory_path, minutes_threshold=1440):
    """
    Clean up old files in the specified directory based on filenames with timestamps.

    Args:
        directory_path (str or Path): The directory path where files are located.
        minutes_threshold (int): The age threshold in minutes for files to be considered old.
            Default is 1440 minutes (1 day).
    """
    directory_path = Path(directory_path)
    threshold_duration = timedelta(minutes=minutes_threshold)
    current_time = datetime.now()

    for file_path in directory_path.iterdir():
        if file_path.is_file():
            # Extract the timestamp part from the filename
            filename_without_extension = os.path.splitext(file_path.name)[0]
            timestamp_part = filename_without_extension.split('_')[-1]

            try:
                # Parse the timestamp from the filename
                file_timestamp = datetime.strptime(timestamp_part, "%Y%m%d%H%M%S")

                if current_time - file_timestamp > threshold_duration:
                    # File is older than the threshold, delete it
                    print(f"Deleting file: {file_path}")
                    file_path.unlink()

            except ValueError:
                # Skip files with invalid or missing timestamps
                pass



