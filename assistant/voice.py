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
        input_rate = 44100
        target_rate = 16000

        audio = sd.rec(
            int(seconds * input_rate),
            samplerate=input_rate,
            channels=1,
            dtype="float32",
        )
        sd.wait()

        samples = np.asarray(audio[:, 0], dtype=np.float32)
        new_length = int(len(samples) * target_rate / input_rate)
        old_indices = np.arange(len(samples))
        new_indices = np.linspace(0, len(samples) - 1, new_length)
        samples = np.interp(new_indices, old_indices, samples)

        pcm = np.clip(samples, -1, 1)
        pcm = (pcm * 32767).astype(np.int16)

        recognizer = KaldiRecognizer(self.model, target_rate)
        recognizer.AcceptWaveform(pcm.tobytes())
        result = json.loads(recognizer.FinalResult())
        return result.get("text", "").strip()
