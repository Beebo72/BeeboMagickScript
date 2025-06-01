import os
import subprocess
from pathlib import Path
from tqdm import tqdm

INPUT_VIDEO = "c:\\Users\\Beebo\\Downloads\\video4917965384755184901.mp4"  # replace path
OUTPUT_VIDEO = "c:\\Users\\Beebo\\wh44arr4r.mp4"  # replace path
TEMP_DIR = Path("temp_frames")
TEMP_AUDIO = Path("wha4r.aac")  # replace name
FILTER = "charcoal:2"  # Example ImageMagick filter

def extract_frames_and_audio(input_video, output_folder, audio_file):
    output_folder.mkdir(parents=True, exist_ok=True)
    # Extract frames
    subprocess.run([
        "ffmpeg", "-i", input_video,
        str(output_folder / "frame_%05d.png")
    ], check=True)
    # Extract audio
    subprocess.run([
        "ffmpeg", "-i", input_video,
        "-vn", "-acodec", "copy",
        str(audio_file)
    ], check=True)


def apply_imagemagick_filter(input_folder, filter_name):
    frames = sorted(input_folder.glob("frame_*.png"))
    for frame in tqdm(frames, desc="Applying ImageMagick"):
        subprocess.run([
            "magick", str(frame),
            "-swirl", "110",  # Change this to other effects
            str(frame)
        ], check=True)

def reassemble_video(input_folder, output_video, audio_file):
    subprocess.run([
        "ffmpeg",
        "-framerate", "30",  # Set FPS as needed
        "-i", str(input_folder / "frame_%05d.png"),
        "-i", str(audio_file),
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-strict", "experimental",
        "-shortest",  # Ensure video doesn't outlast audio
        output_video
    ], check=True)

def cleanup(folder, audio_file):
    for f in folder.glob("*.png"):
        f.unlink()
    folder.rmdir()
    if audio_file.exists():
        audio_file.unlink()

def main():
    extract_frames_and_audio(INPUT_VIDEO, TEMP_DIR, TEMP_AUDIO)
    apply_imagemagick_filter(TEMP_DIR, FILTER)
    reassemble_video(TEMP_DIR, OUTPUT_VIDEO, TEMP_AUDIO)
    # cleanup(TEMP_DIR, TEMP_AUDIO)  # Uncomment to delete temp files after done

if __name__ == "__main__":
    main()
