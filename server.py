from flask import Flask, jsonify

app = Flask(__name__)


def dashboard_state(jarvis):
    return {
        "status": jarvis.ui.status.get() if jarvis.ui else "JARVIS OFFLINE",
        "command": jarvis.ui.last_command.get() if jarvis.ui else "",
        "response": jarvis.ui.response.get() if jarvis.ui else "",
    }


def create_server(jarvis):
    @app.get("/api/status")
    def status():
        return jsonify(dashboard_state(jarvis))

    return app
