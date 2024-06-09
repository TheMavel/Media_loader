import os
import re
import subprocess
import sys
from time import sleep
from pathlib import Path
from PyQt5 import QtWidgets, QtCore
from pytube import YouTube
from pydub import AudioSegment
from mutagen.easyid3 import EasyID3
from mutagen.flac import FLAC
from subprocess import call

def install(package):
    """Installs the given package using pip."""
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Install required packages if not present
try:
    import pytube
    import pydub
    import mutagen
    import spotdl
    import scdl
except ImportError:
    install("pytube")
    install("pydub")
    install("mutagen")
    install('spotdl')
    install('scdl')

def extract_metadata(title):
    match = re.match(r"(.+) - (.+) \[(.+)\]", title)
    if match:
        artist = match.group(1).strip()
        track_title = match.group(2).strip()
        label = match.group(3).strip()
    else:
        artist = "Unknown Artist"
        track_title = title.strip()
        label = "Unknown Label"
    return track_title, artist, label

def download_youtube(url, quality, progress_callback):
    """Downloads audio from YouTube and saves it in the specified format."""
    try:
        yt = YouTube(url, on_progress_callback=progress_callback)
        stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
        temp_file = stream.download(output_path=".")
        title = yt.title
        track_title, artist, label = extract_metadata(title)
        filename = f"{artist} - {track_title}"

        audio = AudioSegment.from_file(temp_file)
        if quality == "WAV":
            new_file = f"{filename}.wav"
            audio.export(new_file, format="wav")
            audio_file = FLAC(new_file)
        elif quality == 'FLAC':
            new_file = f"{filename}.flac"
            audio.export(new_file, format="flac")
            audio_file = FLAC(new_file)
        else:
            new_file = f"{filename}.mp3"
            audio.export(new_file, format="mp3", bitrate="320k")
            audio_file = EasyID3(new_file)

        audio_file['title'] = track_title
        audio_file['artist'] = artist
        if quality != 'WAV':
            audio_file['album'] = label
        audio_file.save()

        os.remove(temp_file)
        return new_file
    except Exception as e:
        return f"Error downloading from YouTube: {e}"

class ProgressBar(QtCore.QObject):
    progress_update = QtCore.pyqtSignal(int)

def update_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize if stream.filesize is not None else 1
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    progress_var.progress_update.emit(int(percentage_of_completion))

def download_spotify(url):
    """Downloads a track from Spotify."""
    try:
        call(["spotdl", url])
    except Exception as e:
        return f"Error downloading from Spotify: {e}"

def download_soundcloud(url):
    """Downloads a track from SoundCloud."""
    try:
        call(["scdl", "-l", url, "--path", "."])
    except Exception as e:
        return f"Error downloading from SoundCloud: {e}"

def search_music(query):
    """Placeholder function for searching music."""
    # Implement API calls to fetch search results
    results = [query]  # Example result
    return results

class MusicDownloaderApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        global progress_var
        global progress_bar

        # Search Bar
        self.search_bar = QtWidgets.QLineEdit(self)
        self.search_bar.setPlaceholderText("Search for tracks or playlists...")
        self.search_bar.setGeometry(10, 10, 280, 30)

        # Search Button
        self.search_button = QtWidgets.QPushButton("Search", self)
        self.search_button.setGeometry(300, 10, 80, 30)
        self.search_button.clicked.connect(self.search_music)

        # Results List
        self.results_list = QtWidgets.QListWidget(self)
        self.results_list.setGeometry(10, 50, 370, 100)

        # Add to Queue Button
        self.add_button = QtWidgets.QPushButton("Add to Queue", self)
        self.add_button.setGeometry(10, 160, 150, 30)
        self.add_button.clicked.connect(self.add_to_queue)

        # Queue Listbox
        self.queue_listbox = QtWidgets.QListWidget(self)
        self.queue_listbox.setGeometry(10, 200, 370, 150)

        # Quality Selection
        self.quality_label = QtWidgets.QLabel("Select Quality:", self)
        self.quality_label.setGeometry(10, 360, 100, 30)
        self.quality_combo = QtWidgets.QComboBox(self)
        self.quality_combo.setGeometry(120, 360, 100, 30)
        self.quality_combo.addItems(["MP3", "WAV", "FLAC"])

        # Process Queue Button
        self.process_button = QtWidgets.QPushButton("Download Queue", self)
        self.process_button.setGeometry(240, 360, 150, 30)
        self.process_button.clicked.connect(self.process_queue)

        # Progress Bar
        progress_var = ProgressBar()
        progress_bar = QtWidgets.QProgressBar(self)
        progress_bar.setGeometry(10, 400, 370, 30)
        progress_bar.setMaximum(100)
        progress_var.progress_update.connect(progress_bar.setValue)  # Connect signal to progress bar

        # Status Label
        self.status_label = QtWidgets.QLabel(self)
        self.status_label.setGeometry(10, 440, 370, 30)

        self.setGeometry(300, 300, 400, 480)
        self.setWindowTitle("Music Downloader")
        self.show()

    def search_music(self):
        query = self.search_bar.text()
        results = search_music(query)
        self.results_list.clear()
        self.results_list.addItems(results)

    def add_to_queue(self):
        selected_items = self.results_list.selectedItems()
        for item in selected_items:
            self.queue_listbox.addItem(item.text())

    def process_queue(self):
        """Processes the download queue."""
        while self.queue_listbox.count() > 0:
            item = self.queue_listbox.takeItem(0)
            track = item.text()
            self.status_label.setText(f"Downloading {track}...")
            result = None
            quality = self.quality_combo.currentText()

            if "youtube.com" in track or "youtu.be" in track:
                result = download_youtube(track, quality, update_progress)
            elif "spotify.com" in track:
                result = download_spotify(track)
            elif "soundcloud.com" in track:
                result = download_soundcloud(track)

            if result and "Error" in result:
                self.status_label.setText(result)
            else:
                self.status_label.setText(f"Downloaded {track}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    downloader = MusicDownloaderApp()
    sys.exit(app.exec_())
