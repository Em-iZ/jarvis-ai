import datetime
import subprocess
import webbrowser


def handle_command(command: str) -> str:
    text = command.lower().strip()

    if text in {"pomoč", "help"}:
        return "Ukazi: odpri chrome, odpri beležnico, odpri kalkulator, odpri youtube, odpri google, ura, izhod"

    if text in {"ura", "koliko je ura", "koliko je ura?"}:
        return datetime.datetime.now().strftime("Trenutni čas je %H:%M.")

    if "youtube" in text:
        webbrowser.open("https://www.youtube.com")
        return "Odpiram YouTube."

    if "google" in text:
        webbrowser.open("https://www.google.com")
        return "Odpiram Google."

    if "chrome" in text:
        try:
            subprocess.Popen(["cmd", "/c", "start", "", "chrome"])
            return "Odpiram Chrome."
        except Exception:
            return "Chroma nisem mogel odpreti."

    if "beležnico" in text or "beležnica" in text or "notepad" in text:
        subprocess.Popen(["notepad.exe"])
        return "Odpiram Beležnico."

    if "kalkulator" in text or "calculator" in text:
        subprocess.Popen(["calc.exe"])
        return "Odpiram Kalkulator."

    return "Tega ukaza še ne znam. Poskusi 'pomoč'."
