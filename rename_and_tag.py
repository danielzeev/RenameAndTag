import os
import subprocess
import sys
import shutil
import venv
import tempfile
import argparse

def run_script_in_venv(venv_dir, audio_path, toc_path, rename_files):
    """
    Writes and executes a Python script inside the virtual environment.
    
    This script performs optional file renaming and metadata updates for MP3 files
    using the specified directory path and table of contents file.
    
    Args:
        venv_dir     : (str) Path to the virtual environment.
        audio_path     : (str) Directory containing MP3 files.
        toc_path     : (str) Path to the table of contents text file.
        rename_files : (bool) Whether to rename MP3 files based on the TOC file.
    """
    # `nt` for windows
    python_executable = os.path.join(
        venv_dir, "Scripts" if os.name == "nt" else "bin", "python" 
    )

    # Escape paths and values
    audio_path = audio_path.replace("\\", "\\\\")
    toc_path = toc_path.replace("\\", "\\\\")
    rename_files = str(rename_files)

    script_code = f'''
import os
import re
from pathlib import Path
from mutagen.easyid3 import EasyID3
import mutagen

AUDIO_PATH   = r"{audio_path}"
CH_TEXT_PATH = r"{toc_path}"
RENAME_FILES = {rename_files}

def rename_file_names():
    """
    Renames MP3 files in AUDIO_PATH based on chapter titles from CH_TEXT_PATH.
    """
    folder    = Path(AUDIO_PATH)
    mp3_files = sorted(folder.glob("*.mp3"))

    with open(CH_TEXT_PATH, "r", encoding="utf-8") as infile:
        toc = [f.strip() for f in infile.readlines()]

    toc = [f"{{i:03d}} {{fname}}" for i, fname in enumerate(toc, start=1)]

    for file, fname in zip(mp3_files, toc):
        ext = file.suffix
        new_name = f"{{fname}}{{ext}}"
        new_path = file.with_name(new_name)
        file.rename(new_path)
        print(f"Renamed: {{file.name}} → {{new_name}}")

def clean_title(filename):
    """
    Removes leading numbers and separators from a filename to clean up the title.
    
    Args:
        filename : (str) The original filename.
        
    Returns:
        str: A cleaned version of the filename.
    """
    name = os.path.splitext(filename)[0]
    cleaned = re.sub(r'^\\d+[\\s\\-_]*', '', name)
    return cleaned

def update_titles_in_folder(folder_path):
    """
    Updates the ID3 'title' metadata tag for each MP3 file in the folder using the filename.
    
    Args:
        folder_path : (str) Directory containing MP3 files.
    """
    for filename in sorted(os.listdir(folder_path)):
        if filename.lower().endswith('.mp3'):
            full_path = os.path.join(folder_path, filename)
            title = clean_title(filename)
            try:
                audio = EasyID3(full_path)
            except mutagen.id3.ID3NoHeaderError:
                audio = mutagen.File(full_path, easy=True)
                audio.add_tags()
            audio['title'] = title
            audio.save()
            print(f"Updated title for '{{filename}}' → '{{title}}'")

if RENAME_FILES:
    rename_file_names()

update_titles_in_folder(AUDIO_PATH)
'''

    # Temporarily write the embedded script to a .py file
    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".py") as script_file:
        script_file.write(script_code)
        script_path = script_file.name

    try:
        # Install the mutagen package inside the venv.
        subprocess.check_call([python_executable, "-m", "pip", "install", "mutagen"])
        # Execute the embedded script using the venv Python
        subprocess.check_call([python_executable, script_path])
    finally:
        # Delete the temporary Python script file that was written
        os.remove(script_path)

def main():
    """
    Parses command-line arguments, sets up a temporary virtual environment,
    and runs the audio processing script inside the environment.
    
    Cleans up the environment when finished.
    """
    parser = argparse.ArgumentParser(description="Rename MP3 files and/or update metadata titles in a virtual environment.")
    parser.add_argument("--audio_path",     required=True,       help="Path to folder containing MP3 files.")
    parser.add_argument("--toc_path",     required=False,      help="Path to the text file with chapter titles (required if --rename_files is used).")
    parser.add_argument("--rename_files", action="store_true", help="Rename MP3 filenames using chapter titles from the TOC file.")
    args = parser.parse_args()

    if args.rename_files and not args.toc_path:
        parser.error("--toc_path is required when using --rename_files")

    # Create a unique temporary directory for the virtual environment.
    venv_dir = tempfile.mkdtemp(prefix="auto_venv_")
    print(f"Creating virtual environment in {venv_dir}")

    try:
        # Initialize venv and install pip
        venv.create(venv_dir, with_pip=True)
        run_script_in_venv(venv_dir, args.audio_path, args.toc_path or "", args.rename_files)
    finally:
        # Delete the virtual environment
        print(f"Deleting virtual environment {venv_dir}")
        shutil.rmtree(venv_dir)

if __name__ == "__main__":
    main()
