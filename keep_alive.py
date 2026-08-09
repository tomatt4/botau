from flask import Flask, render_template_string, jsonify
from threading import Thread
import time
import os

app = Flask(__name__)

start_time = time.time()
bot_instance = None

def format_uptime(seconds):
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)
    return f"{days}d {hours}h {minutes}min"

def get_ping():
    if bot_instance:
        return round(bot_instance.latency * 1000)
    return None

@app.route("/")
def home():
    return "Celestia online!"

@app.route("/api/status")
def api_status():
    ping = get_ping()
    return jsonify({
        "online": True,
        "uptime": format_uptime(time.time() - start_time),
        "ping": ping if ping is not None else "Indisponível",
        "port": os.getenv("PORT", "desconhecida")
    })

def run():
    port = int(os.environ.get("PORT", 10000))
    print(f"🌐 Flask rodando na porta {port}")
    app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)

def keep_alive(bot=None):
    global bot_instance
    bot_instance = bot

    server = Thread(target=run)
    server.start()
