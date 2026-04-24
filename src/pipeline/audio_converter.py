import logging
import yt_dlp
import os

from src.config import FFMPEG_PATH
from src.config import DATA_DIR

logger = logging.getLogger(__name__)

class AudioConverter:
    """Utility for downloading and converting audio from video URLs"""

    def __init__(self):
        """Initialize the AudioConverter"""
        self.ffmpeg_path = FFMPEG_PATH

    def download_audio(self, video_url, output_filename, output_path=DATA_DIR):
        # Convert pathlib.Path to string if needed
        output_path = str(output_path)
        
        # Ensure output directory exists
        os.makedirs(output_path, exist_ok=True)

        # Create full output template path
        output_template = os.path.join(output_path, output_filename + ".%(ext)s")
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_template,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'ffmpeg_location': self.ffmpeg_path  # Specify the path to ffmpeg
        }
        
        try:
            audio_output_path = os.path.join(output_path, output_filename + ".mp3")
            logger.info(f"Downloading audio from {video_url} to {audio_output_path}")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
            logger.info(f"Download completed: {audio_output_path}")
            return audio_output_path
        except Exception as e:
            logger.error(f"Error downloading audio: {e}")
            raise e
        

