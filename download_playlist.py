import csv
import subprocess
import time
import os
from pathlib import Path
from ytmusicapi import YTMusic

OUTPUT_DIR = str(Path.home() / "Music")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_csv_path() -> Path:
    while True:
        user_input = input("Enter CSV path: ").strip()
        csv_path = Path(user_input).expanduser()

        if not user_input:
            print("Error: path cannot be empty")
            continue

        if not csv_path.exists():
            print(f"Error: file not found: {csv_path}")
            continue 
        if not csv_path.is_file():
            print("Error: the specified path is not a file.")
            continue
        if csv_path.suffix.lower() != ".csv":
            print("Error: please select a csv file")
            continue
        return csv_path

# --- Настройки ---
CSV_FILE   = get_csv_path()
DELAY      = 2
# -----------------

os.makedirs(OUTPUT_DIR, exist_ok=True)
ytmusic = YTMusic()

REQUIRED_COLUMNS = {
        "Track Name",
        "Artist Name(s)",
        "Album Name",
        }


def read_playlist(csv_path: Path) -> list[dict]:
    try:
        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            if not reader.fieldnames:
                raise ValueError("CSV file is empty or has no header")

            missing = REQUIRED_COLUMNS - set(reader.fieldnames)

            if missing:
                raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")

            tracks = []
            for line_number, row in enumerate(reader, start=2):
                name   = (row.get("Track Name") or "").strip()
                artist = (row.get("Artist Name(s)") or "").strip()
                album  = (row.get("Album Name") or "").strip()

                if not name or not artist:
                    print(
                        f"Warning: skipping incomplete row"
                        f"{line_number}."
                        )
                    continue
                tracks.append({
                    "name": name,
                    "artist": artist.split(", ")[0].strip(),
                    "album": album
                    })
        if not tracks:
             raise ValueError("No valid tracks found in CSV.")
        return tracks
    except UnicodeDecodeError as error:
        raise ValueError(
            "Could not read the file as UTF-8. Check its encoding."
        ) from error

    except csv.Error as error:
        raise ValueError(
            f"Could not parse CSV: {error}"
        ) from error

    except OSError as error:
        raise ValueError(
            f"Could not open or read the file: {error}"
        ) from error


def search_on_ytmusic(name: str, artist: str) -> str | None:
    query = f"{artist} - {name}"
    try:
        results = ytmusic.search(query, filter="songs", limit=5)
        if not results:
            results = ytmusic.search(query, limit=5)
    except Exception as e:
        print(f"    ⚠ Ошибка поиска: {e}")
        return None

    if not results:
        print(f"    ✗ Не найдено: {query}")
        return None

    video_id = results[0].get("videoId")
    if not video_id:
        print(f"    ✗ Нет videoId: {query}")
        return None

    found_title  = results[0].get("title", "?")
    found_artist = results[0]["artists"][0].get("name", "") if results[0].get("artists") else ""
    print(f"    → {found_artist} - {found_title}")
    return f"https://music.youtube.com/watch?v={video_id}"


def download(url: str, title: str, artist: str, album: str):
    # Имя файла строим сами, без спецсимволов
    safe_name = f"{artist} - {title}".replace("/", "-").replace("\\", "-").replace(":", "-").replace("*", "").replace("?", "").replace('"', "").replace("<", "").replace(">", "").replace("|", "")
    out_template = os.path.join(OUTPUT_DIR, f"{safe_name}.%(ext)s")

    cmd = [
        "yt-dlp",
        "--cookies-from-browser", "firefox",
        url,
        "--format", "bestaudio/best",
        "--output", out_template,
        "--extract-audio",
        "--audio-format", "mp3",
        "--audio-quality", "0",
        "--embed-thumbnail",
        "--add-metadata",
        "--parse-metadata", f":{title}:%(title)s",
        "--no-playlist",
        "--quiet",
        "--progress",
    ]
    result = subprocess.run(cmd)
    return result.returncode == 0


def main():
    try:
        tracks = read_playlist(CSV_FILE)
    except ValueError as error:
        print(f"CSV error: {error}")
        return

    print(f"Плейлист загружен: {len(tracks)} треков\n{'='*50}")

    success, failed = [], []

    for i, t in enumerate(tracks, 1):
        label = f"{t['artist']} - {t['name']}"
        print(f"\n[{i}/{len(tracks)}] {label}")

        url = search_on_ytmusic(t["name"], t["artist"])
        if not url:
            failed.append(label)
            continue

        ok = download(url, t["name"], t["artist"], t["album"])
        if ok:
            success.append(label)
            print(f"    ✓ Скачано")
        else:
            failed.append(label)
            print(f"    ✗ Ошибка при скачивании")

        time.sleep(DELAY)

    print(f"\n{'='*50}")
    print(f"Готово: {len(success)}/{len(tracks)} скачано")
    if failed:
        print("\nНе удалось скачать:")
        for t in failed:
            print(f"  - {t}")


if __name__ == "__main__":
    main()
