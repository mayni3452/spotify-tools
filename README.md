# Music Downloader

A simple Python tool to search for music using YouTube Music and download audio with `yt-dlp`.

The project contains two scripts:
- `download_track.py` — search for and download a single track.
- `download_playlist.py` — download tracks from a CSV playlist exported from Spotify using Exportify.

## Features

- Search for tracks using YouTube Music.
- Download audio in MP3 format.
- Embed thumbnails and metadata.
- Download multiple tracks from a CSV file.
- Handle missing or invalid CSV data.

## Requirements

- Python 3.11 or newer recommended.
- `ffmpeg` installed on your system.
- Firefox, with a browser profile accessible to `yt-dlp`, if using browser cookies.
- A CSV playlist exported using Exportify for playlist downloads.

## Installation

No compilation is required. The scripts run directly with Python 3.

### 1. Clone the repository

Replace `USERNAME` and `REPOSITORY` with your GitHub username and repository name.

```bash
git clone https://github.com/mayni3452/spotify-tools.git
cd spotify-tools
```

Alternatively, download the repository as a ZIP file from GitHub and extract it.

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

Activate it on Linux:

```bash
source .venv/bin/activate
```

### 3. Install Python dependencies

Make sure your `requirements.txt` contains the required packages:

```text
ytmusicapi
yt-dlp
```

Then install them:

```bash
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

### 4. Install ffmpeg

`ffmpeg` is required for audio extraction and MP3 conversion.

On Debian or Ubuntu:

```bash
sudo apt install ffmpeg
```

On Arch Linux:

```bash
sudo pacman -S ffmpeg
```

For other distributions, use your system's package manager.

## Usage

Activate the virtual environment first if it is not already active:

```bash
source .venv/bin/activate
```

### Download a single track

Run:

```bash
python3 download_track.py
```

Follow the prompts and enter the track information when requested.

### Download a playlist from CSV

Run:

```bash
python3 download_playlist.py
```

Enter the path to your CSV file when prompted.

The CSV should contain these columns:

- `Track Name`
- `Artist Name(s)`
- `Album Name`

Export your playlist with Exportify and provide the path to the exported CSV file.

## Browser cookies

The download scripts use Firefox cookies through `yt-dlp`. This may require Firefox to be installed and a browser profile that `yt-dlp` can access.

If downloading fails because of browser-cookie access, check the error message and your Firefox profile configuration.

**Never upload browser cookies, authentication data, or personal files to GitHub.**

## Output

Downloaded files are saved to the `Music` directory inside your home directory, depending on the paths configured in the scripts.

## Troubleshooting

### `python3: command not found`

Install Python 3 using your Linux distribution's package manager.

### `ffmpeg` is missing

Install `ffmpeg` and verify that it is available in your system's `PATH`.

### A Python module is missing

Activate your virtual environment and run:

```bash
python3 -m pip install -r requirements.txt
```

### The CSV file cannot be read

Check that the file is a valid CSV export and contains all required column headers.

### A track cannot be found or downloaded

Search results may not always match the requested track. Check the track title, artist, network connection, and any error reported by `yt-dlp`.

## Legal notice

This project is intended for educational and personal use. Only download content you are legally allowed to download. Respect copyright law, the terms of the services you use, and the rights of content creators.

## License

If you want others to use, modify, and redistribute this project, add a `LICENSE` file to the repository. For example, you can choose the MIT License if that suits your goals.
