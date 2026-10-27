import subprocess
import os
import sys
from ytmusicapi import YTMusic

OUTPUT_DIR = "~/Music"
os.makedirs(OUTPUT_DIR, exist_ok=True)

ytmusic = YTMusic()


def search_and_download(query: str):
    print(f"Ищу: {query}")

    results = ytmusic.search(query, filter="songs", limit=5)
    if not results:
        results = ytmusic.search(query, limit=5)
    if not results:
        print("✗ Не найдено")
        return

    track = results[0]
    title  = track.get("title", "Unknown")
    artist = track["artists"][0]["name"] if track.get("artists") else "Unknown"
    album  = track["album"]["name"] if track.get("album") else ""
    url    = f"https://music.youtube.com/watch?v={track['videoId']}"

    print(f"→ {artist} - {title}")

    safe_name = f"{artist} - {title}".replace("/", "-").replace("\\", "-").replace(":", "-").replace("*", "").replace("?", "").replace('"', "").replace("<", "").replace(">", "").replace("|", "")
    out_template = os.path.join(OUTPUT_DIR, f"{safe_name}.%(ext)s")

    cmd = [
        "yt-dlp", "--cookies-from-browser", "firefox", 
        url,
        "--format", "bestaudio/best",
        "--output", out_template,
        "--extract-audio",
        "--audio-format", "mp3",
        "--audio-quality", "0",
        "--embed-thumbnail",
        "--add-metadata",
        "--no-playlist",
        "--quiet",
        "--progress",
    ]

    result = subprocess.run(cmd)
    if result.returncode == 0:
        print(f"✓ Сохранено: {safe_name}.mp3")
    else:
        print("✗ Ошибка при скачивании")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # запуск из терминала: python download_track.py "Pink Floyd - Comfortably Numb"
        search_and_download(" ".join(sys.argv[1:]))
    else:
        # интерактивный режим
        query = input("Трек > ").strip()
        if query:
            search_and_download(query)
