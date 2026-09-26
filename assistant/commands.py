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
        "koliko je ura trenutno",
        "time",
        "what time is it",
        "what's the time",
        "what time is it now",
        "current time",
    }:
        return datetime.datetime.now().strftime("The current time is %H:%M.")

    if text in {
        "danes",
        "kateri dan je danes",
        "datum",
        "današnji datum",
        "today",
        "date",
        "what is the date",
        "what's the date",
        "what is today's date",
    }:
        return datetime.datetime.now().strftime("Today's date is %d.%m.%Y.")

    if text in {
        "kdo si",
        "kdo si ti",
        "who are you",
        "what are you",
    }:
        return "I am JARVIS, your local AI assistant."

    if text in {
        "status",
        "system status",
        "stanje",
    }:
        return "JARVIS is online and ready for commands."

    # Web commands must be handled before the Windows app launcher.
    if "youtube" in text:
        webbrowser.open("https://www.youtube.com")
        return "Opening YouTube."

    if "google" in text:
        webbrowser.open("https://www.google.com")
        return "Opening Google."

    if (
        "beležnico" in text
        or "beležnica" in text
        or "notepad" in text
    ):
        subprocess.Popen(["notepad.exe"])
        return "Opening Notepad."

    if "kalkulator" in text or "calculator" in text:
        subprocess.Popen(["calc.exe"])
        return "Opening Calculator."

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

    return "I don't know that command yet. Try 'help'."
