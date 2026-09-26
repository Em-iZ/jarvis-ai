import os
import threading

from assistant.commands import handle_command
from ui import JarvisUI
from server import create_server


class Jarvis:
    def __init__(self):
        self.ui = None
        self.voice = None
        self.running = True
        self.voice_lock = threading.Lock()

    def process(self, command: str):
        if not command:
            return
        self.ui.set_command(f"Ti: {command}")
        response = handle_command(command)
        self.ui.set_response(response)
        if self.voice:
            try:
                self.voice.speak(response)
            except Exception:
                pass

    def create_voice(self):
        if self.voice is not None:
            return True
        try:
            from assistant.voice import VoiceEngine
            self.ui.set_status("NALAGAM ANGLEŠKI GLAS ...")
            self.voice = VoiceEngine()
            return True
        except Exception as exc:
            self.ui.set_status(f"GLAS NI NA VOLJO: {type(exc).__name__}")
            self.ui.set_response(
                "JARVIS deluje, vendar glas trenutno ni na voljo. "
                "Preveri mikrofon in namestitev."
            )
            return False

    def _remove_wake_word(self, text: str) -> str:
        wake_words = ("jarvis", "jervis", "džarvis", "džervis")
        for word in wake_words:
            if word in text:
                return text.replace(word, "", 1).strip(" ,.!?")
        return ""

    def voice_loop(self):
        with self.voice_lock:
            if not self.create_voice():
                return

            self.ui.set_status("ČAKAM NA: WAKE UP JARVIS")
            active = False

            while self.running:
                try:
                    heard = self.voice.listen(4)
                    if not heard:
                        continue

                    self.ui.set_command(f"Slišim: {heard}")
                    low = heard.lower().strip()

                    if not active:
                        if "wake up jarvis" in low or "wake up jervis" in low:
                            active = True
                            self.ui.set_status("JARVIS AKTIVEN")
                            self.voice.speak("I'm listening.")
                        elif any(word in low for word in ("jarvis", "jervis", "džarvis", "džervis")):
                            active = True
                            command = self._remove_wake_word(low)
                            self.ui.set_status("JARVIS AKTIVEN")
                            if command:
                                self.process(command)
                            else:
                                self.voice.speak("I'm listening.")
                        continue

                    command = self._remove_wake_word(low)
                    if command:
                        self.process(command)
                        self.ui.set_status("JARVIS AKTIVEN")

                except Exception as exc:
                    self.ui.set_status(f"GLAS: {type(exc).__name__}")
                    self.ui.set_response(
                        "Glasovni del se je ustavil. JARVIS ostaja odprt."
                    )
                    return

    def listen_once(self):
        # Kept for the GUI button: starts the same continuous voice loop.
        threading.Thread(target=self.voice_loop, daemon=True).start()

    def start(self):
        # Start the web dashboard on the local network.
        web_app = create_server(self)
        threading.Thread(
            target=lambda: web_app.run(
                host="0.0.0.0",
                port=5000,
                debug=False,
                use_reloader=False,
            ),
            daemon=True,
        ).start()

        self.ui = JarvisUI(self.process, self.close, self.listen_once)
        self.ui.set_response(
            "JARVIS je pripravljen. Pritisni POSLUŠAJ za glasovni test."
        )
        self.ui.run()

    def close(self):
        self.running = False
        if self.ui:
            self.ui.root.destroy()


if __name__ == "__main__":
    Jarvis().start()
