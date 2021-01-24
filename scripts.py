"""Temporary functions to be migrated into processes / database work."""
import os
import csv


def add_notes_files(thumbs_directory: str) -> None:
    """For each subdirectory with photos in (without subdirectories), add a csv file with
    photonames, tag field and notes field.
    
    If file already exists extend for any files that are not in the csv."""

    targets = {}

    for subdir, dirs, files in os.walk(thumbs_directory):
        for file in files:
            if dirs:
                continue
            try:
                targets[subdir].append(file)
            except KeyError:
                targets[subdir] = []

    for path, files in targets.items():
        note_filename = os.path.join(path, "notes.csv")
        if os.path.exists(note_filename) is False:
            # Setup the empty file if not exists
            with open(note_filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['File', 'Tags', 'Notes'])
        # Extract the existing filenames
        with open(note_filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            existing_names = [row[0] for row in reader]
        # Write new filenames to the file
        with open(note_filename, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for filename in files:
                if filename in existing_names:
                    continue
                writer.writerow([filename, '', ''])
    return
