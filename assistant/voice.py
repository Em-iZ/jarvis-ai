import os
import tempfile
import wave

import numpy as np
import pyttsx3
import sounddevice as sd
from faster_whisper import WhisperModel


class VoiceEngine:
    def __init__(self):
        model_name = os.getenv("JARVIS_MODEL", "small")
        self.model = WhisperModel(model_name, device="cpu", compute_type="int8")
        self.tts = pyttsx3.init()
        self.tts.setProperty("rate", 175)
        self.tts.setProperty("volume", 1.0)

    def speak(self, text: str):
        self.tts.say(text)
        self.tts.runAndWait()

    def listen(self, seconds: float = 4.0) -> str:
        rate = 16000
        audio = sd.rec(
            int(seconds * rate),
            samplerate=rate,
            channels=1,
            dtype="float32",
        )
        sd.wait()

        pcm = np.clip(audio[:, 0], -1, 1)
        pcm = (pcm * 32767).astype(np.int16)

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            path = tmp.name

        try:
            with wave.open(path, "wb") as wav:
                wav.setnchannels(1)
                wav.setsampwidth(2)
                wav.setframerate(rate)
                wav.writeframes(pcm.tobytes())

            segments, _ = self.model.transcribe(
                path,
                language="sl",
                vad_filter=True,
                beam_size=1,
            )
            return " ".join(s.text.strip() for s in segments).strip()
        finally:
            try:
                os.remove(path)
            except OSError:
                pass
