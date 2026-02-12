import discord
import os
import sys
import asyncio
from discord.ext import commands
from dotenv import load_dotenv

# Add the project root to sys.path to allow imports from 'bot' package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()


class RizeBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(
            command_prefix=".",
            intents=intents,
            help_command=None,
            activity=discord.Game(name="Lumi | /help")
        )

    async def setup_hook(self):
        # Load extensions/cogs
        await self.load_extension("cogs.moderation")
        await self.load_extension("cogs.admin")
        await self.load_extension("cogs.random_number")
        await self.load_extension("cogs.lembrete")
        await self.load_extension("cogs.utils")
        await self.load_extension("cogs.afk")
        await self.load_extension("cogs.assumir")
        await self.load_extension("cogs.codigo_conduta")
        await self.load_extension("cogs.gestao_staff")
        await self.load_extension("cogs.mensagem")
        await self.load_extension("cogs.embeds")
        print("Lumi: Cogs carregados")
        # Sync slash commands
        await self.tree.sync()
        print("Lumi: Comandos sincronizados brother")

    async def on_ready(self):
        print(f"Conectado: {self.user} (ID: {self.user.id})")
        print("------")

bot = RizeBot()
bot.run("MTQ1NzQxMjQ0NDg0NTY0MTgxMQ.GLR4SL.F5XBsO67u71DRxidMO7eQ6Y-oe3A52DyGlOgSQ")