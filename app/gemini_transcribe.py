from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import List

import google.generativeai as genai


@dataclass
class TranscriptSegment:
    index: int
    start_seconds: float
    end_seconds: float
    text: str


def _format_srt_timestamp(seconds: float) -> str:
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def write_srt(segments: List[TranscriptSegment], output_path: str | Path) -> Path:
    path = Path(output_path)
    lines: List[str] = []
    for seg in segments:
        lines.append(str(seg.index))
        lines.append(f"{_format_srt_timestamp(seg.start_seconds)} --> {_format_srt_timestamp(seg.end_seconds)}")
        lines.append(seg.text)
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def configure_gemini_from_env() -> None:
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise EnvironmentError("GOOGLE_API_KEY is not set")
    genai.configure(api_key=api_key)


def transcribe_audio_with_gemini(
    audio_file: str | Path,
    model_name: str = "gemini-1.5-pro",
) -> str:
    configure_gemini_from_env()

    model = genai.GenerativeModel(model_name)
    audio_path = Path(audio_file)
    if not audio_path.exists():
        raise FileNotFoundError(f"Audio not found: {audio_path}")

    # File API: upload and reference in prompt
    uploaded = genai.upload_file(path=str(audio_path))

    prompt = (
        "以下の音声の正確な逐語文字起こしを日本語で作成してください。"
        "句読点を適切に付与し、不要なノイズ語は括弧で明示してください。"
    )

    response = model.generate_content([
        {"text": prompt},
        uploaded,
    ])
    transcription = response.text or ""

    # Best-effort cleanup
    return transcription.strip()


def naive_chunk_to_segments(text: str, chunk_seconds: float = 5.0) -> List[TranscriptSegment]:
    # Since Gemini response lacks timestamps natively, produce naive fixed-size segments
    words = text.split()
    words_per_chunk = max(1, int(20 * (chunk_seconds / 5)))
    segments: List[TranscriptSegment] = []
    start = 0.0
    idx = 1
    for i in range(0, len(words), words_per_chunk):
        chunk_words = words[i : i + words_per_chunk]
        end = start + chunk_seconds
        segments.append(TranscriptSegment(index=idx, start_seconds=start, end_seconds=end, text=" ".join(chunk_words)))
        start = end
        idx += 1
    return segments

