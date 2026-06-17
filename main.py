import discord
from discord.ext import commands
import os
from keep_alive import keep_alive
import random
from discord.ext import tasks

status_list = [
    "dis.gg/ccdv | /ia",
    "Hakari AI v1.0.2",
    "Assistente IA a sua disposição.",
    "Não tenho outros comandos, apenas o /ia!",
    "O bot principal é o Hakari#4021.",
    "Fui feito em Python por Salva.",
    "A API que uso é a do Groq, sabia?"
]

@tasks.loop(minutes=1)
async def trocar_status():
    await bot.change_presence(status=discord.Status.idle, activity=discord.CustomActivity(name=random.choice(status_list)))

# Intents
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=",", intents=intents)
    
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
        
    if not trocar_status.is_running():
        trocar_status.start()

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
        keep_alive(bot)
        await load_cogs()
        await bot.start(os.getenv("DISCORD_TOKEN"))

import asyncio

asyncio.run(main())
