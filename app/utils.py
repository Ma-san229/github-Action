import os
import subprocess
from pathlib import Path
from typing import Optional
import shutil
import imageio_ffmpeg


def ensure_directory_exists(path: str | Path) -> Path:
    output_path = Path(path)
    output_path.mkdir(parents=True, exist_ok=True)
    return output_path


def run_ffmpeg_extract_audio(
    input_video: str | Path,
    output_audio: str | Path,
    sample_rate_hz: int = 16000,
    channels: int = 1,
    overwrite: bool = True,
) -> Path:
    input_path = Path(input_video)
    output_path = Path(output_audio)
    if not input_path.exists():
        raise FileNotFoundError(f"Input video not found: {input_path}")

    ensure_directory_exists(output_path.parent)
    if overwrite and output_path.exists():
        output_path.unlink()

    ffmpeg_bin = shutil.which("ffmpeg") or imageio_ffmpeg.get_ffmpeg_exe()
    cmd = [
        ffmpeg_bin,
        "-y" if overwrite else "-n",
        "-i",
        str(input_path),
        "-vn",
        "-acodec",
        "pcm_s16le",
        "-ac",
        str(channels),
        "-ar",
        str(sample_rate_hz),
        str(output_path),
    ]

    process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if process.returncode != 0:
        raise RuntimeError(f"ffmpeg failed: {process.stderr}")
    return output_path

