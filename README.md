# RenameAndTag

RenameAndTag is a Python utility that automates renaming audiobook MP3 files (or other MP3 files) using a chapter list and updating the MP3 ID3 metadata title tags to match their filenames. It runs all operations inside a temporary Python virtual environment, keeping your system clean and dependency-free.

---

## Features

- ✅ Rename MP3 files using a plain `.txt` table of contents (TOC).
- ✅ Clean up and update MP3 ID3 title metadata automatically.
- ✅ Runs in a temporary virtual environment — no system-wide installs.
- ✅ Cross-platform support (Windows, macOS, Linux).

---

## Input Requirements

To use the `--rename_files` option, you must supply a **plain text file** with chapter titles — one title per line. This file will be used to rename the MP3 files **in order**.

---

## Requirements

- Python 3.6 or newer
- Access to the command line / terminal

---

## Usage

1. Clone or download this repository.

2. Prepare your audiobook folder with MP3 files.  
   Example: `./some_audiobook/`

3. (Optional) Create a TOC text file listing chapter titles line-by-line.  
   Example: `some_audiobook_toc.txt`

4. Run the script from your terminal:

### Update metadata titles only (no renaming)

```bash
python rename_and_tag.py --audio_path "./some_audiobook"
````

### Rename files and update metadata titles

```bash
python rename_and_tag.py --audio_path "./some_audiobook" --toc_path "some_audiobook_toc.txt" --rename_files
```

---

## Command Line Arguments

| Argument         | Description                                                   | Required?                      |
| ---------------- | ------------------------------------------------------------- | ------------------------------ |
| `--book_path`    | Path to folder containing MP3 files.                          | ✅ Required                    |
| `--toc_path`     | Path to TOC `.txt` file with chapter titles.                  | ✅ If `--rename_files` is used |
| `--rename_files` | Include this flag to rename MP3 filenames using the TOC file. | Optional                       |

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

