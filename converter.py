import os
import re
import yt_dlp

def extract_playlist_id(url):
    match = re.search(r"[?&]list=([a-zA-Z0-9_-]+)", url)
    return match.group(1) if match else None

def download_playlist_mp3(playlist_url, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'noplaylist': False,
        'quiet': False,
        'ignoreerrors': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([playlist_url])

def main():
    url = input("Inserisci l'URL della playlist YouTube: ").strip()
    playlist_id = extract_playlist_id(url)

    if not playlist_id:
        print("❌ URL non valido o mancante del parametro 'list='.")
        return

    print(f"✅ Playlist ID: {playlist_id}")
    output_folder = f"playlist_{playlist_id}_mp3"
    download_playlist_mp3(url, output_folder)
    print("\n✅ Download completato.")

if __name__ == "__main__":
    main()

