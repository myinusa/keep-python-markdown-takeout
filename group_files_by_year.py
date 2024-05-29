import logging
import os
import re
import shutil
import sys
from datetime import datetime


def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
    )


def validate_args():
    if len(sys.argv) != 3 or sys.argv[1] != "--input-dir":
        logging.error("Usage: script.py --input-dir <directory>")
        sys.exit(1)
    input_dir = sys.argv[2]
    if not os.path.isdir(input_dir):
        logging.error(f"Provided input directory does not exist: {input_dir}")
        sys.exit(1)
    return input_dir


def find_markdown_files(input_dir):
    markdown_files = []
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".md"):
                markdown_files.append(os.path.join(root, file))
    return markdown_files


def group_files_by_year(markdown_files):
    grouped_files = {}
    date_pattern = re.compile(r"^(\d{4})-(\d{2})-(\d{2})")
    for file in markdown_files:
        filename = os.path.basename(file)
        match = date_pattern.match(filename)
        if match:
            year = match.group(1)
            if year not in grouped_files:
                grouped_files[year] = []
            grouped_files[year].append(file)
    return grouped_files


def create_directories_and_move_files(grouped_files, input_dir):
    for year, files in grouped_files.items():
        year_dir = os.path.join(input_dir, year)
        if not os.path.exists(year_dir):
            os.makedirs(year_dir)
        for file in files:
            try:
                shutil.move(file, year_dir)
                logging.info(f"Moved {file} to {year_dir}")
            except Exception as e:
                logging.error(f"Error moving file {file} to {year_dir}: {e}")


def main():
    setup_logging()
    input_dir = validate_args()
    markdown_files = find_markdown_files(input_dir)
    grouped_files = group_files_by_year(markdown_files)
    create_directories_and_move_files(grouped_files, input_dir)


if __name__ == "__main__":
    main()
