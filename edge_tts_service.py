"""
edge_tts_service.py  —  Microsoft Edge Neural TTS for manim-voiceover

Uses the same Azure Neural voices as Microsoft Edge browser.
Completely free, no API key required.

Default voice: en-US-AndrewNeural
  Other good choices for academic narration:
    en-US-ChristopherNeural  (measured, authoritative)
    en-GB-RyanNeural         (professional British)
    en-US-GuyNeural          (clear, natural male)

Usage in a scene:
    from edge_tts_service import EdgeTTSService
    self.set_speech_service(EdgeTTSService())          # default voice
    self.set_speech_service(EdgeTTSService(voice="en-GB-RyanNeural"))
"""

import asyncio
from pathlib import Path

from manim_voiceover.services.base import (
    PathLike,
    SpeechService,
    initialize_speech_service,
    path_to_string,
)
from manim_voiceover.helper import remove_bookmarks
from manim_voiceover._typing import VoiceoverData

try:
    import edge_tts
except ImportError:
    raise ImportError(
        "edge-tts is not installed. Run:  pip install edge-tts"
    )


class EdgeTTSService(SpeechService):
    """SpeechService using Microsoft Edge Neural TTS (free, no API key)."""

    def __init__(self, voice: str = "en-US-AndrewNeural", **kwargs):
        """
        Args:
            voice: Edge TTS voice name.
                   Run `edge-tts --list-voices` to see all options.
        """
        initialize_speech_service(self, kwargs)
        self.voice = voice

    def generate_from_text(
        self,
        text: str,
        cache_dir: PathLike | None = None,
        path: PathLike | None = None,
        **kwargs,
    ) -> VoiceoverData:
        if cache_dir is None:
            cache_dir = self.cache_dir

        input_text = remove_bookmarks(text)
        input_data = {"input_text": input_text, "service": f"edge_tts_{self.voice}"}

        cached = self.get_cached_result(input_data, cache_dir)
        if cached is not None:
            return cached

        if path is None:
            audio_path = self.get_audio_basename(input_data) + ".mp3"
        else:
            audio_path = path_to_string(path)

        full_path = str(Path(cache_dir) / audio_path)

        async def _synthesise():
            communicate = edge_tts.Communicate(input_text, self.voice)
            await communicate.save(full_path)

        asyncio.run(_synthesise())

        return {
            "input_text": text,
            "input_data": input_data,
            "original_audio": audio_path,
        }
