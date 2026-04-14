# Video & Audio Transcriber

A simple tool to transcribe locally saved MP4 videos, MP3 audio files, or YouTube videos to text using OpenAI's Whisper model and ffmpeg.

## Features

- Process individual MP4 video files or entire directories
- Process individual MP3 audio files or entire directories
- Process individual YouTube video URLs
- Extract audio from video using ffmpeg
- Transcribe audio using OpenAI's Whisper model
- Save transcriptions as text (`.txt`) files
- Support for different Whisper model sizes (tiny, base, small, medium, large). Default model is small.

## Requirements

- Python 3.10+
- ffmpeg installed on your system
- Required Python packages (install via `pip install -r requirements.txt`):
  - openai-whisper
  - yt-dlp

## Installation

1. Clone this repository:
   ```
   git clone <repository-url>
   cd video-audio-transcriber
   ```

2. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Ensure ffmpeg is installed on your system:
   - **macOS**: `brew install ffmpeg`
   - **Ubuntu/Debian**: `sudo apt-get install ffmpeg`
   - **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html)

---

## Video Transcription

### Basic Usage

Drop your MP4 files into the `videos/` folder, then run:

```
python transcribe.py
```

This will:
1. Look for all MP4 files in the `videos` directory
2. Extract audio from each video using ffmpeg
3. Transcribe the audio using the Whisper model
4. Save transcriptions as `.txt` files in the `output` directory

### Command-line Options

- `--video`: Transcribe a single video file
  ```
  python transcribe.py --video path/to/your/video.mp4
  ```

- `--videos_dir`: Specify a custom directory of videos (default: `videos`)
  ```
  python transcribe.py --videos_dir path/to/video/directory
  ```

- `--output_dir`: Specify a custom output directory (default: `output`)
  ```
  python transcribe.py --output_dir path/to/output/directory
  ```

- `--model`: Specify the Whisper model size (default: `small`)
  ```
  python transcribe.py --model medium
  ```

### Examples

Transcribe a specific video using the medium model:
```
python transcribe.py --video videos/lecture.mp4 --model medium
```

Transcribe all videos in a custom directory:
```
python transcribe.py --videos_dir my_videos --output_dir my_transcripts
```

---

## Audio Transcription

### Basic Usage

Drop your MP3 files into the `audios/` folder, then run:

```
python transcribe.py --mode audio
```

This will:
1. Look for all MP3 files in the `audios` directory
2. Transcribe each audio file using the Whisper model
3. Save transcriptions as `.txt` files in the `output` directory

### Command-line Options

- `--audio`: Transcribe a single MP3 file
  ```
  python transcribe.py --audio path/to/your/audio.mp3
  ```

- `--audios_dir`: Specify a custom directory of MP3 files (default: `audios`)
  ```
  python transcribe.py --mode audio --audios_dir path/to/audio/directory
  ```

- `--output_dir`: Specify a custom output directory (default: `output`)
  ```
  python transcribe.py --mode audio --output_dir path/to/output/directory
  ```

- `--model`: Specify the Whisper model size (default: `small`)
  ```
  python transcribe.py --mode audio --model medium
  ```

### Examples

Transcribe a specific MP3 file:
```
python transcribe.py --audio audios/interview.mp3
```

Transcribe all MP3s in the default audios folder using the large model:
```
python transcribe.py --mode audio --model large
```

Transcribe all MP3s in a custom folder:
```
python transcribe.py --mode audio --audios_dir my_recordings --output_dir my_transcripts
```

---

## YouTube Transcription

### Basic Usage

Pass a YouTube URL directly:

```
python transcribe.py --url "https://www.youtube.com/watch?v=VIDEO_ID"
```

This will:
1. Download the audio-only stream from the YouTube video
2. Transcribe it using the Whisper model
3. Save the transcript as a `.txt` file in the `output` directory, named after the video title
4. Clean up the temporary audio file automatically

### Command-line Options

- `--url`: The YouTube video URL (required for this mode)
  ```
  python transcribe.py --url "https://www.youtube.com/watch?v=VIDEO_ID"
  ```

- `--model`: Specify the Whisper model size (default: `small`)
  ```
  python transcribe.py --url "https://www.youtube.com/watch?v=VIDEO_ID" --model medium
  ```

- `--output_dir`: Specify a custom output directory (default: `output`)
  ```
  python transcribe.py --url "https://www.youtube.com/watch?v=VIDEO_ID" --output_dir my_transcripts
  ```

### Examples

Transcribe a YouTube video using the medium model:
```
python transcribe.py --url "https://www.youtube.com/watch?v=VIDEO_ID" --model medium
```

You can also use `--mode youtube` explicitly alongside `--url`:
```
python transcribe.py --mode youtube --url "https://www.youtube.com/watch?v=VIDEO_ID"
```

> **Note:** Only single videos are supported. Playlist URLs will be treated as a single video (the playlist is ignored).

---

## Directory Structure

```
VideoAudioTranscriber/
├── videos/       # Place MP4 video files here for batch processing
├── audios/       # Place MP3 audio files here for batch processing
├── output/       # Transcription .txt files are saved here
└── transcribe.py
```

> YouTube mode downloads a temporary `yt_temp_audio.mp3` into `output/` during processing and deletes it automatically once transcription is complete.

## Notes

- For large files, transcription may take time depending on your hardware
- The `large` model provides the most accurate transcription but requires more computational resources
- Available model sizes: `tiny`, `base`, `small` (default), `medium`, `large`

## Acknowledgements

- [openai/whisper](https://github.com/openai/whisper) — speech recognition model used for transcription
- [ffmpeg](https://ffmpeg.org) — used for audio extraction from video files
- [harliandi/video-transcriber](https://github.com/harliandi/video-transcriber) — referenced for video transcription approach
- [javedali99/audio-to-text-transcription](https://github.com/javedali99/audio-to-text-transcription?tab=readme-ov-file) — referenced for audio transcription approach
