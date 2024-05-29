import argparse  # Import argparse module
import glob
import json
import logging
import os
import re
import shutil  # Import shutil for directory operations
from datetime import datetime, timezone
from os.path import join

from rich.traceback import install

install()

abs_dir = os.path.dirname(os.path.abspath(__file__))

# Constants
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
MARKDOWN_TEMPLATE = "# {title}\n\n{content}"
ISO_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"
markdown_dir_path = join(abs_dir, "data/markdown")
os.makedirs(markdown_dir_path, exist_ok=True)

# Set up logging
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

# Define constants
JSON_FILE_EXTENSION = ".json"
MARKDOWN_FILE_EXTENSION = ".md"

def clear_directory(directory):
    """Remove all files in the specified directory."""
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            logging.error(f"Failed to delete {file_path}. Reason: {e}")


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Convert Google Keep JSON files to Markdown."
    )
    parser.add_argument("--input_dir", type=str, help="Directory containing JSON files")
    args = parser.parse_args()

    # Use the input directory provided by the user
    json_dir = getattr(args, "input_dir")  # Access the 'input_dir' attribute

    # Clear the markdown directory before starting
    clear_directory(markdown_dir_path)
    logging.info("Cleared markdown directory.")

    # Find all JSON files in the directory
    json_files = glob.glob(join(json_dir, f"*{JSON_FILE_EXTENSION}"))
    print(f"Found {len(json_files)} JSON files.")

    # Perform a dry run to ensure all JSON files are valid
    for index, file_path in enumerate(json_files):
        try:
            with open(file_path, "r") as file:
                json.load(file)
        except json.JSONDecodeError:
            logging.error(f"Invalid JSON file [Index {index + 1}: {file_path}]")

    # Process each JSON file
    for index, file_path in enumerate(json_files):
        with open(file_path, "r") as file:
            data = json.load(file)

        # Extract relevant fields from the JSON data with error handling
        try:
            text_content = data.get(
                "textContent", ""
            )  # Use empty string if "textContent" is missing
            title = data.get(
                "title", "NoTitle"
            )  # Use empty string if "title" is missing
            labels = [
                label["name"] for label in data.get("labels", [])
            ]  # Use empty list if "labels" is missing
        except KeyError as e:
            logging.error(
                f"Error extracting data from JSON file [Index {index + 1}: {file_path}]: {e}"
            )
            continue  # Skip processing this file

        created_timestamp_usec = int(data["createdTimestampUsec"]) / 1e6
        user_edited_timestamp_usec = int(data["userEditedTimestampUsec"]) / 1e6

        # Convert user-edited timestamp to the desired date format
        formatted_modified_date = datetime.fromtimestamp(
            user_edited_timestamp_usec, timezone.utc
        ).strftime("%A, %B %w %Y, %H:%M %p")

        formatted_created_date = datetime.fromtimestamp(
            created_timestamp_usec, timezone.utc
        ).strftime("%A, %B %w %Y, %H:%M %p")

        created_filename_date = datetime.fromtimestamp(
            created_timestamp_usec, timezone.utc
        ).strftime("%Y-%m-%d-%H-%M")

        # Define a maximum length for filenames
        MAX_FILENAME_LENGTH = 255  # Adjust based on your filesystem limits, typically 255 characters for most systems

        # Replace all non-alphanumeric characters with '_'
        title = re.sub(r"\W+", "_", title)

        # Truncate the title to ensure the filename length does not exceed the maximum allowed
        max_title_length = (
            MAX_FILENAME_LENGTH
            - len(created_filename_date)
            - len(MARKDOWN_FILE_EXTENSION)
            - 1
        )  # Subtract lengths of date, extension, and hyphen
        if len(title) > max_title_length:
            title = title[:max_title_length]

        # Create the Markdown file name
        markdown_file_name = f"{created_filename_date}-{title}{MARKDOWN_FILE_EXTENSION}"

        # Write the Markdown content
        try:
            with open(
                join(markdown_dir_path, markdown_file_name), "w+"
            ) as markdown_file:
                # YAML front matter
                markdown_file.write("---\n")
                markdown_file.write(f"title: {title}\n")
                markdown_file.write(f"date created: {formatted_created_date}\n")
                markdown_file.write(f"date modified: {formatted_modified_date}\n")
                markdown_file.write("---\n\n")
                # Markdown content
                markdown_file.write(f"### {title}\n\n")
                for label in labels:
                    markdown_file.write(f"* {label}\n")
                markdown_file.write(f"\n{text_content}")
                logging.info(
                    f"Markdown file '{markdown_file_name}' created successfully. [Index {index + 1}]"
                )
        except Exception as e:
            logging.error(f"Error writing to file '{markdown_file_name}': {e}")
            raise


if __name__ == "__main__":
    main()
