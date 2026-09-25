import json
import subprocess
import webbrowser


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


def open_app(name: str) -> str:
    name = name.strip()
    if not name:
        return "Povej mi ime aplikacije."

    apps = _start_apps()
    wanted = name.casefold()

    exact = next(
        (app for app in apps if app.get("Name", "").casefold() == wanted),
        None,
    )
    match = exact or next(
        (app for app in apps if wanted in app.get("Name", "").casefold()),
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
        url = name if name.startswith(("http://", "https://")) else f"https://{name}"
        webbrowser.open(url)
        return f"Odpiram {name}."

    return f"Aplikacije '{name}' ne najdem med aplikacijami Windows."


def find_apps(query: str):
    query = query.casefold().strip()
    return [
        app.get("Name", "")
        for app in _start_apps()
        if query in app.get("Name", "").casefold()
    ][:10]
