import discord
from discord.ext import commands
from discord import app_commands
import os
import sys
from flask import Flask
from threading import Thread
import asyncio
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
PORT = int(os.getenv("PORT", 8080))

if not TOKEN:
    print("❌ ERRO: DISCORD_TOKEN não encontrado!")
    sys.exit(1)

app = Flask(__name__)

@app.route("/")
def health_check():
    return {"status": "Bot Celestia is running"}, 200

@app.route("/health")
def health():
    return {"status": "ok"}, 200


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix=["c.", "/"],
    intents=intents
)


# =========================
# BOT ONLINE
# =========================

@bot.event
async def on_ready():
    print(f"✅ {bot.user} está online!")

    try:
        synced = await bot.tree.sync()

        print(f"✅ {len(synced)} slash command(s) sincronizado(s)!")

        for command in synced:
            print(f"   → /{command.name}")

    except Exception as e:
        print(f"❌ Erro ao sincronizar slash commands: {e}")


# =========================
# CARREGAR COGS
# =========================

async def load_cogs():

    cogs_dir = "./cogs"

    if not os.path.exists(cogs_dir):
        print(f"⚠️ Pasta {cogs_dir} não encontrada!")
        return

    for filename in os.listdir(cogs_dir):

        if filename.endswith(".py") and not filename.startswith("_"):

            try:

                await bot.load_extension(
                    f"cogs.{filename[:-3]}"
                )

                print(f"✅ Cog carregada: {filename}")

            except Exception as e:

                print(f"❌ Erro ao carregar {filename}: {e}")


# =========================
# INICIAR BOT
# =========================
async def main():
    
    await load_cogs()
    
    await bot.start(TOKEN)


# =========================
# FLASK
# =========================

def run_flask():

    print(f"🚀 Servidor web rodando na porta {PORT}")

    app.run(
        host="0.0.0.0",
        port=PORT,
        debug=False
    )


# =========================
# EXECUTAR
# =========================

if __name__ == "__main__":

    flask_thread = Thread(
        target=run_flask,
        daemon=True
    )

    flask_thread.start()

    try:

        asyncio.run(main())

    except KeyboardInterrupt:

        print("\n⏹️ Bot desligado pelo usuário")

    except Exception as e:

        print(f"❌ Erro fatal: {e}")
        sys.exit(1)
