from __future__ import annotations

from pathlib import Path
from gtts import gTTS
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, TIT2, TALB, TPE1, COMM


def synthesize_podcast_mp3(text: str, output_mp3: str | Path, lang: str = "ja") -> Path:
    out_path = Path(output_mp3)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    tts = gTTS(text=text, lang=lang)
    tts.save(str(out_path))
    return out_path


def tag_mp3(
    mp3_path: str | Path,
    title: str,
    album: str = "AIニュースポッドキャスト",
    artist: str = "AutoNarrator",
    comment: str | None = None,
) -> None:
    path = Path(mp3_path)
    if not path.exists():
        return
    try:
        audio = ID3(str(path))
    except Exception:
        audio = ID3()

    audio.add(TIT2(encoding=3, text=title))
    audio.add(TALB(encoding=3, text=album))
    audio.add(TPE1(encoding=3, text=artist))
    if comment:
        audio.add(COMM(encoding=3, lang='jpn', desc='Comment', text=comment))
    audio.save(str(path))

