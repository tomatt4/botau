import discord
from discord.ext import commands
import os
import flask
import threading

# Intents
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=",", intents=intents)

# =========================
# SERVIDOR FLASK
# =========================

app = flask.Flask(__name__)

@app.route("/")
def home():
    return "Bot está online!"

def run_flask():
    app.run(host="0.0.0.0", port=8080)

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

# =========================
# CARREGAR COGS
# =========================

async def load_cogs():
    for file in os.listdir("./cogs"):
        if file.endswith(".py"):
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
