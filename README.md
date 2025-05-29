# RenameAndTag: MP3 File Renamer and Metadata Updater

This Python script automates renaming audiobook chapter MP3 files (or other MP3 files) based on a table of contents (TOC) text file, and/or updating the MP3 ID3 metadata titles to match their filenames. It runs all operations inside a temporary Python virtual environment to keep dependencies isolated and clean.

---

## Features

- **Optional filename renaming** based on a TOC text file (chapter titles).
- **Metadata title updating** for MP3 files, cleaning out leading track numbers.
- Automatic creation and cleanup of a **temporary Python virtual environment**.
- No manual dependency installation needed — `mutagen` is installed automatically in the venv.
- Cross-platform support (Windows, macOS, Linux).

---

## Requirements

- Python 3.6 or newer
- Access to the command line / terminal

---

## Usage

1. Clone or download this repository.

2. Prepare your audiobook folder with MP3 files.  
   Example: `./some_audiobook/`

3. Prepare a TOC text file listing chapter titles line-by-line (optional).  
   Example: `some_audiobook_toc.txt`

4. Run the script from your terminal:

### Update metadata titles only (no renaming)

```bash
python process_audio.py --audio_path "./some_audiobook"
````

### Rename files and update metadata titles

```bash
python process_audio.py --audio_path "./some_audiobook" --toc_path "some_audiobook_toc.txt" --rename_files
```

---

## Command Line Arguments

| Argument         | Description                                 | Required/Optional                    |
| ---------------- | ------------------------------------------- | ------------------------------------ |
| `--audio_path`    | Path to folder containing MP3 files         | Required                             |
| `--toc_path`     | Path to TOC text file with chapter titles   | Required if `--rename_files` is used |
| `--rename_files` | Flag to rename MP3 filenames using TOC file | Optional                             |

---

## How It Works

* The script creates a **temporary virtual environment**.
* Installs the `mutagen` package inside it.
* Generates and runs a Python script that:

  * Optionally renames MP3 files based on the TOC file.
  * Updates the ID3 `title` tags using the cleaned filenames.
* Deletes the virtual environment on completion.

---

## License

MIT License — feel free to modify and use as you like.

---

