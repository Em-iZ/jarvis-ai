import json
import os
import urllib.request


class LocalAI:
    def __init__(self):
        self.model = os.getenv("JARVIS_AI_MODEL", "gemma4:26b")
        self.url = os.getenv(
            "JARVIS_OLLAMA_URL",
            "http://127.0.0.1:11434/api/generate",
        )

    def ask(self, prompt: str) -> str:
        payload = {
            "model": self.model,
            "prompt": (
                "Ti si JARVIS, lokalni AI pomočnik. "
                "Odgovarjaj v slovenščini, razen če uporabnik govori v drugem jeziku. "
                "Bodi naraven, prijazen in jedrnat. "
                "Ne omenjaj, da si Gemma, razen če uporabnik to izrecno vpraša.\n\n"
                f"Uporabnik: {prompt}\nJARVIS:"
            ),
            "stream": False,
            "options": {
                "temperature": 0.7,
            },
        }

        data = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            self.url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urllib.request.urlopen(request, timeout=180) as response:
                result = json.loads(response.read().decode("utf-8"))
            answer = result.get("response", "").strip()
            return answer or "Trenutno nimam odgovora."
        except Exception:
            return (
                "Povezava z lokalnim AI modelom trenutno ni na voljo. "
                "Preveri, ali Ollama deluje."
            )
