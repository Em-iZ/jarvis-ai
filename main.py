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

    def listen_once(self):
        with self.voice_lock:
            if not self.create_voice():
                return

            try:
                self.ui.set_status("POSLUŠAM ...")
                heard = self.voice.listen(6)
                if not heard:
                    self.ui.set_response("Nisem ničesar slišal.")
                    return

                self.ui.set_command(f"Slišim: {heard}")
                low = heard.lower().strip()
                wake_words = ("jarvis", "jervis", "džarvis", "džervis")

                for word in wake_words:
                    if word in low:
                        low = low.replace(word, "", 1).strip(" ,.!?")
                        break

                if not low:
                    self.voice.speak("Da?")
                    low = self.voice.listen(6)

                if low:
                    self.process(low)
            except Exception as exc:
                self.ui.set_status(f"GLAS: {type(exc).__name__}")
                self.ui.set_response(
                    "Glasovni del se ni zagnal. JARVIS ostaja odprt."
                )
            finally:
                self.ui.set_status("JARVIS ONLINE")

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

        # Voice is initialized only when needed. This prevents a microphone/
        # audio-driver problem from closing the whole application at startup.
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
