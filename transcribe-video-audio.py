import os
import re
import argparse
import whisper
import subprocess
import yt_dlp
from pathlib import Path


def ensure_directory_exists(directory):
    """Create directory if it doesn't exist."""
    os.makedirs(directory, exist_ok=True)


def sanitize_filename(title):
    """Convert a video title to a safe filesystem filename (no extension)."""
    sanitized = re.sub(r'[\\/:*?"<>|]+', '', title)
    sanitized = re.sub(r'[\s.]+', '_', sanitized).strip('_')
    return sanitized[:200] if sanitized else "youtube_transcription"


def extract_audio(video_path, audio_path):
    """Extract audio from video file using ffmpeg."""
    try:
        command = [
            "ffmpeg",
            "-i", video_path,
            "-q:a", "0",
            "-map", "a",
            "-y",  # Overwrite output files without asking
            audio_path
        ]
        
        # Run the ffmpeg command
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Audio extracted successfully to {audio_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error extracting audio: {e}")
        return False


def download_youtube_audio(url, output_dir):
    """Download audio from a YouTube URL and convert to MP3. Returns (audio_path, title) or (None, None)."""
    temp_name = "yt_temp_audio"
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(output_dir, f"{temp_name}.%(ext)s"),
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "noplaylist": True,
        "quiet": True,
        "no_warnings": False,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get("title", "youtube_transcription")
        audio_path = os.path.join(output_dir, f"{temp_name}.mp3")
        print(f"Audio downloaded successfully: {title}")
        return audio_path, title
    except yt_dlp.utils.DownloadError as e:
        print(f"Error downloading YouTube audio: {e}")
        return None, None


def transcribe_audio(audio_path, output_path, model_size="base"):
    """Transcribe audio using Whisper model and save as .txt text file."""
    try:
        # Load the Whisper model
        print(f"Loading Whisper model ({model_size})...")
        model = whisper.load_model(model_size)
        
        # Transcribe the audio
        print(f"Transcribing audio file: {audio_path}")
        result = model.transcribe(audio_path)
        
        # Save as .txt text file
        with open(output_path, "w", encoding="utf-8") as file:
            file.write(result["text"])
        
        print(f"Transcription saved to: {output_path}")
        return True
    except Exception as e:
        print(f"Error during transcription: {e}")
        return False


def process_video(video_path, output_dir="output", model_size="base"):
    """Process a single video file: extract audio and transcribe it."""
    # Ensure output directory exists
    ensure_directory_exists(output_dir)
    
    # Create file paths
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    audio_path = os.path.join(output_dir, f"{video_name}.mp3")
    transcript_path = os.path.join(output_dir, f"{video_name}.txt")
    
    # Extract audio using ffmpeg
    if not extract_audio(video_path, audio_path):
        return False
    
    # Transcribe audio using Whisper
    return transcribe_audio(audio_path, transcript_path, model_size)


def process_audio(audio_path, output_dir="output", model_size="base"):
    """Process a single audio MP3 file: transcribe it directly."""
    ensure_directory_exists(output_dir)

    audio_name = os.path.splitext(os.path.basename(audio_path))[0]
    transcript_path = os.path.join(output_dir, f"{audio_name}.txt")

    print(f"Processing audio file: {audio_path}")
    return transcribe_audio(audio_path, transcript_path, model_size)


def process_youtube(url, output_dir="output", model_size="base"):
    """Download a YouTube video's audio and transcribe it."""
    ensure_directory_exists(output_dir)

    audio_path, title = download_youtube_audio(url, output_dir)
    if not audio_path:
        return False

    transcript_path = os.path.join(output_dir, f"{sanitize_filename(title)}.txt")
    try:
        return transcribe_audio(audio_path, transcript_path, model_size)
    finally:
        if os.path.exists(audio_path):
            os.remove(audio_path)


def process_audio_directory(directory_path, output_dir="output", model_size="base"):
    """Process all MP3 files in the specified directory."""
    audio_files = [f for f in os.listdir(directory_path) if f.lower().endswith('.mp3')]

    if not audio_files:
        print(f"No MP3 files found in {directory_path}")
        return

    print(f"Found {len(audio_files)} MP3 files to process")

    for audio_file in audio_files:
        audio_path = os.path.join(directory_path, audio_file)
        print(f"\nProcessing audio: {audio_path}")
        process_audio(audio_path, output_dir, model_size)


def process_directory(directory_path, output_dir="output", model_size="base"):
    """Process all MP4 files in the specified directory."""
    # Get all MP4 files in the directory
    video_files = [f for f in os.listdir(directory_path) if f.lower().endswith('.mp4')]

    if not video_files:
        print(f"No MP4 files found in {directory_path}")
        return

    print(f"Found {len(video_files)} MP4 files to process")

    # Process each video file
    for video_file in video_files:
        video_path = os.path.join(directory_path, video_file)
        print(f"\nProcessing video: {video_path}")
        process_video(video_path, output_dir, model_size)


def main():
    # Create the argument parser
    parser = argparse.ArgumentParser(description="Video and Audio Transcriber Tool")

    # Add arguments
    parser.add_argument(
        "--video", type=str, help="Path to a specific video file to transcribe",
        default=None
    )
    parser.add_argument(
        "--audio", type=str, help="Path to a specific MP3 audio file to transcribe",
        default=None
    )
    parser.add_argument(
        "--videos_dir", type=str, help="Directory containing videos to transcribe",
        default="videos"
    )
    parser.add_argument(
        "--audios_dir", type=str, help="Directory containing MP3 audio files to transcribe",
        default="audios"
    )
    parser.add_argument(
        "--output_dir", type=str, help="Directory for output files",
        default="output"
    )
    parser.add_argument(
        "--model", type=str,
        help="Whisper model size (tiny, base, small, medium, large)",
        default="small"
    )
    parser.add_argument(
        "--url", type=str, help="YouTube URL to download and transcribe",
        default=None
    )
    parser.add_argument(
        "--mode", type=str, choices=["video", "audio", "youtube"], default="video",
        help="Transcription mode: 'video' (default), 'audio', or 'youtube'"
    )

    # Parse the arguments
    args = parser.parse_args()

    # Ensure output directory exists
    ensure_directory_exists(args.output_dir)

    if args.url or args.mode == "youtube":
        if not args.url:
            print("Error: --url is required when using --mode youtube")
            return
        print(f"Processing YouTube URL: {args.url}")
        process_youtube(args.url, args.output_dir, args.model)
    elif args.mode == "audio" or args.audio:
        # Audio transcription mode
        if args.audio:
            if not os.path.exists(args.audio):
                print(f"Error: Audio file not found: {args.audio}")
                return
            print(f"Processing single audio file: {args.audio}")
            process_audio(args.audio, args.output_dir, args.model)
        else:
            if not os.path.exists(args.audios_dir):
                print(f"Error: Audios directory not found: {args.audios_dir}")
                return
            print(f"Processing all audio files in directory: {args.audios_dir}")
            process_audio_directory(args.audios_dir, args.output_dir, args.model)
    else:
        # Video transcription mode
        if args.video:
            if not os.path.exists(args.video):
                print(f"Error: Video file not found: {args.video}")
                return
            print(f"Processing single video: {args.video}")
            process_video(args.video, args.output_dir, args.model)
        else:
            if not os.path.exists(args.videos_dir):
                print(f"Error: Videos directory not found: {args.videos_dir}")
                return
            print(f"Processing all videos in directory: {args.videos_dir}")
            process_directory(args.videos_dir, args.output_dir, args.model)


if __name__ == "__main__":
    main()

# Main execution
