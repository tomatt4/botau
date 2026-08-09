import discord
from discord.ext import commands
import os
import dotenv

# Carregar variáveis de ambiente
dotenv.load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Configuração do bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="c.", intents=intents)

# Evento: Bot conectado
@bot.event
async def on_ready():
    print(f"{bot.user} está online!")
    try:
        synced = await bot.tree.sync()
        print(f"{len(synced)} comando(s) sincronizado(s)")
    except Exception as e:
        print(f"Erro ao sincronizar comandos: {e}")

# Carregar cogs
async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            print(f"Cog carregada: {filename}")

# Função para executar o bot
async def main():
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
