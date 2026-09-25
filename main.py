import threading

from assistant.commands import handle_command
from assistant.voice import VoiceEngine
from ui import JarvisUI


class Jarvis:
    def __init__(self):
        self.ui = None
        self.voice = None
        self.running = True

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

    def voice_loop(self):
        self.ui.set_status("POSLUŠAM ... RECI »JARVIS«")
        while self.running:
            try:
                heard = self.voice.listen(4)
                if not heard:
                    continue
                self.ui.set_command(f"Slišim: {heard}")
                low = heard.lower()
                wake_words = ("jarvis", "jervis", "džarvis", "džervis")
                if any(word in low for word in wake_words):
                    command = low
                    for word in wake_words:
                        command = command.replace(word, "", 1)
                    command = command.strip(" ,.!?")
                    self.ui.set_status("POSLUŠAM UKAZ ...")
                    if not command:
                        self.voice.speak("Da?")
                        command = self.voice.listen(6)
                    if command:
                        self.process(command)
                    self.ui.set_status("POSLUŠAM ... RECI »JARVIS«")
            except Exception as exc:
                self.ui.set_status(f"GLAS: {type(exc).__name__}")

    def start(self):
        self.ui = JarvisUI(self.process, self.close)

        def setup():
            try:
                self.ui.set_status("NALAGAM SLOVENSKI GOVOR ...")
                self.voice = VoiceEngine()
                self.ui.set_status("POSLUŠAM ... RECI »JARVIS«")
                threading.Thread(target=self.voice_loop, daemon=True).start()
            except Exception as exc:
                self.ui.set_status(f"GLAS NI NA VOLJO: {type(exc).__name__}")
                self.ui.set_response(
                    "Preveri mikrofon in namestitev iz requirements.txt."
                )

        threading.Thread(target=setup, daemon=True).start()
        self.ui.run()

    def close(self):
        self.running = False
        self.ui.root.destroy()


if __name__ == "__main__":
    Jarvis().start()
