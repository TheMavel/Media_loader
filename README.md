Overview
The Music Downloader App is a versatile and user-friendly tool designed to help users download audio tracks from popular platforms such as YouTube, Spotify, and SoundCloud. It features a clean interface built with PyQt5, allowing users to search for tracks, add them to a download queue, select their preferred audio format, and track download progress.

Features
Platform Support: Download audio tracks from YouTube, Spotify, and SoundCloud.
Format Selection: Choose between MP3, WAV, and FLAC formats.
Queue Management: Add multiple tracks to a download queue and process them sequentially.
Progress Tracking: Visual progress bar to track the download status.
Metadata Extraction: Automatically tag downloaded files with title, artist, and album information.
Requirements
Python 3.x
PyQt5
PyInstaller
pytube
pydub
mutagen
spotdl
scdl
Installation
Clone the repository:

sh
Copy code
git clone https://github.com/yourusername/music-downloader.git
cd music-downloader
Install dependencies:

sh
Copy code
pip install -r requirements.txt
Run the application:

sh
Copy code
python MLV2.py
Creating an Executable
To create an executable for the application, use PyInstaller:

Generate a spec file:

sh
Copy code
pyinstaller --onefile --specpath . MLV2.py
Modify the spec file (if needed) to include additional data files:

python
Copy code
# Example spec file modifications
datas=[('path/to/data/file', 'destination/path')]
Build the executable:

sh
Copy code
pyinstaller MLV2.spec
Usage
Search for Tracks: Enter a keyword or URL in the search bar and click "Search".
Add to Queue: Select tracks from the search results and click "Add to Queue".
Select Quality: Choose the desired audio format (MP3, WAV, FLAC) from the dropdown menu.
Download Queue: Click "Download Queue" to start downloading the queued tracks. Monitor the progress via the progress bar.
Troubleshooting
Ensure all required libraries are installed.
Verify that the kanwadict4.db file is included when building the executable (for spotdl).
For platform-specific issues, rebuild the executable on the target platform using PyInstaller.
