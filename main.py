import discord
from discord.ext import commands
import os
import flask
import threading
from flask import Flask
from threading import Thread
import random
from discord.ext import tasks

# Intents
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=",", intents=intents)

status_list = [
    "dis.gg/ccdv | /ia",
    "hakari AI v1.0.2"
]

@tasks.loop(minutes=1)
async def trocar_status():
    await bot.change_presence(status=discord.Status.idle, activity=discord.CustomActivity(name=random.choice(status_list)))
    
# =========================
# SERVIDOR FLASK
# =========================

app = flask.Flask(__name__)

@app.route("/")
def home():
    return "Bot está online!"

def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

def keep_alive():
    t = threading.Thread(target=run_flask)
    t.start()

# =========================
# EVENTOS
# =========================

@bot.event
async def on_ready():
    print(f"Logado como {bot.user}")
    print("Bot online!")

    try:
        synced = await bot.tree.sync()
        print(f"✅ Slash commands sincronizados: {len(synced)}")
        print("📜 Comandos:", [cmd.name for cmd in synced])
    except Exception as e:
        print(f"❌ Erro ao sincronizar comandos: {e}")

# =========================
# CARREGAR COGS
# =========================

async def load_cogs():
    base_path = os.path.join(os.path.dirname(__file__), "cogs")

    for file in os.listdir(base_path):
        if file.endswith(".py") and file != "__init__.py":
            await bot.load_extension(f"cogs.{file[:-3]}")

# =========================
# INICIAR BOT
# =========================

async def main():
    async with bot:
        await load_cogs()
        await bot.start(os.getenv("DISCORD_TOKEN"))

keep_alive()

import asyncio
asyncio.run(main())
