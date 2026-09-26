import datetime
import re
import subprocess
import webbrowser

from assistant.app_launcher import open_app


def handle_command(command: str) -> str:
    text = re.sub(r"\s+", " ", command.lower().strip())
    text = text.rstrip("?!.,;:")

    if text in {
        "pomoč",
        "help",
        "kaj znaš",
        "kaj lahko narediš",
        "what can you do",
        "what do you do",
    }:
        return (
            "Lahko odpiram aplikacije in igre, spletne strani ter povem uro in datum. "
            "Reci na primer: odpri Discord, zaženi Steam, open YouTube ali what time is it."
        )

    if text in {
        "ura",
        "koliko je ura",
        "koliko je ura zdaj",
        "what time is it",
        "what's the time",
        "current time",
    }:
        return datetime.datetime.now().strftime("Trenutni čas je %H:%M.")

    if text in {
        "danes",
        "kateri dan je danes",
        "datum",
        "today",
        "what is the date",
        "what's the date",
    }:
        return datetime.datetime.now().strftime("Danes je %d.%m.%Y.")

    if text in {
        "kdo si",
        "kdo si ti",
        "who are you",
        "what are you",
    }:
        return "Sem JARVIS, tvoj lokalni AI pomočnik."

    if text in {
        "status",
        "system status",
        "stanje",
    }:
        return "JARVIS deluje in je pripravljen na ukaze."

    # Web commands must be handled before the Windows app launcher.
    if "youtube" in text:
        webbrowser.open("https://www.youtube.com")
        return "Odpiram YouTube."

    if "google" in text:
        webbrowser.open("https://www.google.com")
        return "Odpiram Google."

    if (
        "beležnico" in text
        or "beležnica" in text
        or "notepad" in text
    ):
        subprocess.Popen(["notepad.exe"])
        return "Odpiram Beležnico."

    if "kalkulator" in text or "calculator" in text:
        subprocess.Popen(["calc.exe"])
        return "Odpiram Kalkulator."

    prefixes = (
        "odpri mi ",
        "odpri ",
        "zaženi mi ",
        "zaženi ",
        "launch ",
        "open ",
        "start ",
        "run ",
    )
    for prefix in prefixes:
        if text.startswith(prefix):
            target = text[len(prefix):].strip()
            if target:
                return open_app(target)

    return "Tega ukaza še ne znam. Poskusi 'pomoč'."
