from flask import Flask, jsonify, render_template_string


app = Flask(__name__)

DASHBOARD_HTML = """
<!doctype html>
<html lang="sl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>JARVIS Dashboard</title>
<style>
* { box-sizing: border-box; }
body {
  margin: 0;
  min-height: 100vh;
  font-family: "Segoe UI", Arial, sans-serif;
  color: #eafcff;
  background:
    radial-gradient(circle at 50% 42%, #12333d 0, #071016 32%, #020509 72%);
  display: flex;
  align-items: center;
  justify-content: center;
}
.panel {
  width: min(1100px, 92vw);
  min-height: 650px;
  padding: 38px;
  border: 1px solid #164552;
  border-radius: 28px;
  background: rgba(3, 10, 15, .78);
  box-shadow: 0 0 55px rgba(60, 220, 255, .12);
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 20px;
}
.logo {
  font-size: 32px;
  font-weight: 800;
  letter-spacing: 10px;
  color: #66e6ff;
}
.status {
  padding: 9px 14px;
  border: 1px solid #1e6170;
  border-radius: 999px;
  color: #7df9ff;
  font-size: 13px;
  font-weight: 700;
}
.clock {
  margin-top: 55px;
  text-align: center;
  font-size: clamp(64px, 10vw, 110px);
  font-weight: 300;
  letter-spacing: 5px;
}
.date {
  text-align: center;
  color: #8fa6b8;
  font-size: 17px;
}
.grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 18px;
  margin-top: 55px;
}
.card {
  padding: 22px;
  min-height: 145px;
  border: 1px solid #123d4a;
  border-radius: 18px;
  background: rgba(8, 22, 29, .7);
}
.label {
  color: #5eafc0;
  font-size: 12px;
  font-weight: 800;
  letter-spacing: 2px;
  text-transform: uppercase;
}
.value {
  margin-top: 15px;
  font-size: 20px;
  line-height: 1.45;
  overflow-wrap: anywhere;
}
.online { color: #7df9ff; }
.offline { color: #ff8b8b; }
@media (max-width: 700px) {
  .panel { padding: 22px; min-height: 100vh; border-radius: 0; }
  .grid { grid-template-columns: 1fr; margin-top: 35px; }
  .header { align-items: flex-start; flex-direction: column; }
}
</style>
</head>
<body>
<main class="panel">
  <div class="header">
    <div class="logo">JARVIS</div>
    <div id="status" class="status">CONNECTING...</div>
  </div>

  <div id="clock" class="clock">--:--:--</div>
  <div id="date" class="date">Povezovanje ...</div>

  <section class="grid">
    <div class="card">
      <div class="label">Zadnji ukaz</div>
      <div id="command" class="value">Čakam ...</div>
    </div>
    <div class="card">
      <div class="label">JARVIS odgovor</div>
      <div id="response" class="value">Povezovanje z možgani ...</div>
    </div>
  </section>
</main>

<script>
const statusEl = document.getElementById("status");
const commandEl = document.getElementById("command");
const responseEl = document.getElementById("response");

function updateClock() {
  const now = new Date();
  document.getElementById("clock").textContent =
    now.toLocaleTimeString("sl-SI", {hour12: false});
  document.getElementById("date").textContent =
    now.toLocaleDateString("sl-SI", {
      weekday: "long", day: "2-digit", month: "2-digit", year: "numeric"
    });
}
setInterval(updateClock, 1000);
updateClock();

async function updateDashboard() {
  try {
    const response = await fetch("/api/status", {cache: "no-store"});
    const data = await response.json();

    statusEl.textContent = data.status || "JARVIS ONLINE";
    statusEl.className = "status " +
      ((data.status || "").includes("ONLINE") ? "online" : "offline");

    commandEl.textContent = data.command || "Čakam ...";
    responseEl.textContent = data.response || "Ni odgovora.";
  } catch (error) {
    statusEl.textContent = "POVEZAVA PREKINJENA";
    statusEl.className = "status offline";
  }
}

updateDashboard();
setInterval(updateDashboard, 1000);
</script>
</body>
</html>
"""


def dashboard_state(jarvis):
    return {
        "status": jarvis.ui.status.get() if jarvis.ui else "JARVIS OFFLINE",
        "command": jarvis.ui.last_command.get() if jarvis.ui else "",
        "response": jarvis.ui.response.get() if jarvis.ui else "",
    }


def create_server(jarvis):
    @app.get("/")
    def dashboard():
        return render_template_string(DASHBOARD_HTML)

    @app.get("/api/status")
    def status():
        return jsonify(dashboard_state(jarvis))

    return app
