import yt_dlp
import os
import logging
import shutil
import subprocess

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def download_youtube_audio(url: str) -> str:

    output_path = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path,

        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "192",
            }
        ],

        "quiet": True,
        "noplaylist": True,
        "nocheckcertificate": True,
        "geo_bypass": True,

        "http_headers": {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "en-US,en;q=0.9",
        },

        "extractor_args": {
            "youtube": {
                "player_client": ["android", "web"]
            }
        },
    }

    node_path = shutil.which("node")

    if node_path:
        ydl_opts["js_runtimes"] = {
            "node": {
                "path": node_path
            }
        }

    cookies_from_browser = os.getenv("YTDLP_COOKIES_FROM_BROWSER")
    cookiefile = os.getenv("YTDLP_COOKIEFILE")

    if cookiefile:
        ydl_opts["cookiefile"] = cookiefile

    elif cookies_from_browser:

        if cookies_from_browser == "1":
            ydl_opts["cookiesfrombrowser"] = "chrome"

        else:
            ydl_opts["cookiesfrombrowser"] = cookies_from_browser

    try:

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            info = ydl.extract_info(url, download=True)

            filename = ydl.prepare_filename(info)

            filename = (
                filename
                .replace(".webm", ".wav")
                .replace(".m4a", ".wav")
            )

        return filename

    except Exception as e:
        logging.exception("yt-dlp failed to download URL: %s", url)
        raise


def convert_to_wav(input_path: str) -> str:

    output_path = os.path.splitext(input_path)[0] + "_converted.wav"

    command = [
        "ffmpeg",
        "-y",
        "-i", input_path,
        "-ac", "1",
        "-ar", "16000",
        output_path
    ]

    subprocess.run(command, check=True)

    return output_path


def chunk_audio(wav_path: str, chunk_minutes: int = 10) -> list:

    # Simplified version without pydub
    # Whisper can handle long audio directly

    return [wav_path]


def process_input(source: str) -> list:

    if source.startswith("http://") or source.startswith("https://"):

        print("Detected YouTube URL. Downloading audio...")

        wav_path = download_youtube_audio(source)

    else:

        print("Detected local file. Converting to WAV...")

        wav_path = convert_to_wav(source)

    print("Preparing audio...")

    chunks = chunk_audio(wav_path)

    print(f"Audio ready — {len(chunks)} chunk(s) created.")

    return chunks