import json
import os

import numpy as np
import pyttsx3
import sounddevice as sd
from vosk import KaldiRecognizer, Model


class VoiceEngine:
    def __init__(self):
        model_path = os.getenv(
            "JARVIS_VOSK_MODEL",
            "vosk-model-small-en-us-0.15",
        )
        self.model = Model(model_path)
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

        recognizer = KaldiRecognizer(self.model, rate)
        recognizer.AcceptWaveform(pcm.tobytes())
        result = json.loads(recognizer.FinalResult())
        return result.get("text", "").strip()
