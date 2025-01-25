import os
from os import scandir, rename, makedirs
from os.path import exists, join, splitext
from shutil import move
import logging

# Get the current user's Downloads directory
home_dir = os.path.expanduser("~")
source_dir = os.path.join(home_dir, "Downloads")

# Define destination directories
dest_dir_zip = os.path.join(source_dir, "Archives")
dest_dir_torrent = os.path.join(source_dir, "Torrents")
dest_dir_sfx = os.path.join(source_dir, "SFX")
dest_dir_music = os.path.join(source_dir, "Music")
dest_dir_video = os.path.join(source_dir, "Videos")
dest_dir_image = os.path.join(source_dir, "Images")
dest_dir_documents = os.path.join(source_dir, "Documents")
dest_dir_executable = os.path.join(source_dir, "Executables")

image_extensions = [".jpg", ".jpeg", ".png", ".gif", ".webp", ".tiff", ".bmp", ".heif", ".heic", ".svg", ".ico"]
video_extensions = [".webm", ".mpg", ".mpeg", ".mp4", ".avi", ".mov", ".flv", ".mkv"]
audio_extensions = [".m4a", ".flac", ".mp3", ".wav", ".wma", ".aac"]
document_extensions = [".doc", ".docx", ".odt", ".pdf", ".xls", ".xlsx", ".ppt", ".pptx", ".txt"]
zip_extensions = [".zip", ".7z", ".rar", ".tar", ".gz", ".bz2", ".xz", ".iso"]
exe_extensions = [".exe", ".msi"]
torrent_extensions = [".torrent"]

# Functions
def make_unique(dest, name):
    filename, extension = splitext(name)
    counter = 1
    while exists(f"{dest}/{name}"):
        name = f"{filename}({counter}){extension}"
        counter += 1
    return name

def move_file(dest, entry, name):
    if exists(f"{dest}/{name}"):
        name = make_unique(dest, name)
    move(entry.path, join(dest, name))

def ensure_directories():
    for directory in [dest_dir_sfx, dest_dir_music, dest_dir_video, dest_dir_image, dest_dir_documents]:
        makedirs(directory, exist_ok=True)

def check_file_type(entry, name):
    lower_name = name.lower()
    if any(lower_name.endswith(ext) for ext in audio_extensions):
        dest = dest_dir_sfx if entry.stat().st_size < 10_000_000 or "SFX" in name else dest_dir_music
        move_file(dest, entry, name)
        logging.info(f"Moved audio file: {name}")
    elif any(lower_name.endswith(ext) for ext in video_extensions):
        move_file(dest_dir_video, entry, name)
        logging.info(f"Moved video file: {name}")
    elif any(lower_name.endswith(ext) for ext in image_extensions):
        move_file(dest_dir_image, entry, name)
        logging.info(f"Moved image file: {name}")
    elif any(lower_name.endswith(ext) for ext in document_extensions):
        move_file(dest_dir_documents, entry, name)
        logging.info(f"Moved document file: {name}")
    elif any(lower_name.endswith(ext) for ext in zip_extensions):
        move_file(dest_dir_zip, entry, name)
        logging.info(f"Moved archive file: {name}")
    elif any(lower_name.endswith(ext) for ext in torrent_extensions):
        move_file(dest_dir_torrent, entry, name)
        logging.info(f"Moved torrent file: {name}")
    elif any(lower_name.endswith(ext) for ext in exe_extensions):
        move_file(dest_dir_executable, entry, name)
        logging.info(f"Moved torrent file: {name}")

def on_cleaner():
    with scandir(source_dir) as entries:
        for entry in entries:
            if entry.is_file():
                check_file_type(entry, entry.name)

# Main
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
    ensure_directories()
    on_cleaner()
