import json
import re
import subprocess
import webbrowser

APP_ALIASES = {
    "discord": ("discord",),
    "steam": ("steam",),
    "spotify": ("spotify",),
    "minecraft": ("minecraft",),
    "vs code": ("visual studio code", "vs code", "code"),
    "vscode": ("visual studio code", "vs code", "code"),
    "chrome": ("google chrome", "chrome"),
    "edge": ("microsoft edge", "edge"),
}


def _start_apps():
    ps = (
        "Get-StartApps | "
        "Select-Object Name,AppID | "
        "ConvertTo-Json -Compress"
    )
    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command", ps],
            capture_output=True,
            text=True,
            timeout=8,
        )
        data = json.loads(result.stdout or "[]")
        if isinstance(data, dict):
            data = [data]
        return data
    except Exception:
        return []


def _normalize_name(name: str) -> str:
    name = name.casefold().strip()
    name = re.sub(r"\s+", " ", name)
    return name


def open_app(name: str) -> str:
    name = _normalize_name(name)
    if not name:
        return "Povej mi ime aplikacije."

    apps = _start_apps()
    wanted = name

    aliases = APP_ALIASES.get(wanted, (wanted,))

    exact = next(
        (
            app
            for app in apps
            if _normalize_name(app.get("Name", "")) in aliases
        ),
        None,
    )

    match = exact or next(
        (
            app
            for app in apps
            if any(
                alias in _normalize_name(app.get("Name", ""))
                or _normalize_name(app.get("Name", "")) in alias
                for alias in aliases
            )
        ),
        None,
    )

    if match:
        app_id = match.get("AppID", "")
        try:
            subprocess.Popen(
                ["explorer.exe", f"shell:AppsFolder\\{app_id}"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return f"Odpiram {match.get('Name', name)}."
        except Exception:
            pass

    # Useful for websites said as commands.
    if "." in name and " " not in name:
        url = (
            name
            if name.startswith(("http://", "https://"))
            else f"https://{name}"
        )
        webbrowser.open(url)
        return f"Odpiram {name}."

    return f"Aplikacije '{name}' ne najdem med aplikacijami Windows."


def find_apps(query: str):
    query = _normalize_name(query)
    return [
        app.get("Name", "")
        for app in _start_apps()
        if query in _normalize_name(app.get("Name", ""))
    ][:10]
