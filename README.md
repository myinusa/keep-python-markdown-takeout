# Keep Python Markdown Takeout Google

## Description

 Takes a directory containing Google Keep JSON files as input. It converts each JSON file into a Markdown file, preserving the content, title, labels, creation date, and modification date. The Markdown files are organized in a specified directory for easy access and management.

## Steps

### Run Python Markdown Takeout Google

- Run the following command in the terminal:

```shell
python3 start.py --input_dir /path/to/json/files
```

- Default output directory: `./data/markdown`

- Wait for the conversion to finish

### Export Google Keep

- Visit `https://takeout.google.com/settings/takeout`

<p align="center">
    <img src="./img/image.png" alt="alt text" width="400">
</p>

- Only select `Keep`

<p align="center">
    <img src="./img/image-1.png" alt="alt text" width="400">

</p>

- Select `Export once` for frequency

<p align="center">
    <img src="./img/image-2.png" alt="alt text" width="400">
</p>

- Wait for the export to finish

<p align="center">
    <img src="./img/image-3.png" alt="alt text" width="400">
</p>

- When ready, visit link and download

<p align="center">
    <img src="./img/image-4.png" alt="alt text" width="400">
</p>

## Features

### Group files by year

```shell
python3 group_files_by_year.py --input-dir "./data/markdown"
```

## Roadmap

- [ ] Ability to specify output directory
- [ ] Record installation and Use
- [ ] Setup script for Poetry
- [ ] File Structure
