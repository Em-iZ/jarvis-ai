import datetime
import subprocess
import webbrowser

from assistant.app_launcher import open_app


def handle_command(command: str) -> str:
    text = command.lower().strip()

    if text in {"pomoč", "help", "kaj znaš"}:
        return (
            "Lahko odpiram aplikacije in igre, spletne strani ter povem uro. "
            "Reci na primer: odpri Discord, zaženi Steam, odpri YouTube ali koliko je ura."
        )

    if text in {"ura", "koliko je ura", "koliko je ura?"}:
        return datetime.datetime.now().strftime("Trenutni čas je %H:%M.")

    if text in {"danes", "kateri dan je danes", "datum"}:
        return datetime.datetime.now().strftime("Danes je %d.%m.%Y.")

    prefixes = ("odpri mi ", "odpri ", "zaženi mi ", "zaženi ", "launch ")
    for prefix in prefixes:
        if text.startswith(prefix):
            return open_app(text[len(prefix):])

    if "youtube" in text:
        webbrowser.open("https://www.youtube.com")
        return "Odpiram YouTube."

    if "google" in text:
        webbrowser.open("https://www.google.com")
        return "Odpiram Google."

    if "beležnico" in text or "beležnica" in text or "notepad" in text:
        subprocess.Popen(["notepad.exe"])
        return "Odpiram Beležnico."

    if "kalkulator" in text or "calculator" in text:
        subprocess.Popen(["calc.exe"])
        return "Odpiram Kalkulator."

    return "Tega ukaza še ne znam. Poskusi 'pomoč'."
