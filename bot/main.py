import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

# ========================
# 🔐 ENV
# ========================
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
TEST_GUILD_ID = int(os.getenv("TEST_GUILD_ID"))
PROD_GUILD_ID = int(os.getenv("PROD_GUILD_ID"))

if not TOKEN:
    raise RuntimeError("TOKEN não encontrado")
    
# ========================
# 🌐 KEEP ALIVE
# ========================
keep_alive()

# ========================
# 🧠 INTENTS
# ========================
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# ========================
# 🤖 BOT
# ========================
class DualGuildBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=",",
            intents=intents,
            help_command=None,
            activity=discord.Game(name="TOMEI BAN DA API | /help")
        )

    async def setup_hook(self):
        # 🔹 Cogs essenciais
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
        await self.load_extension("cogs.word_filter")
        await self.load_extension("cogs.welcome")
        await self.load_extension("cogs.antiraid")
        await self.load_extension("cogs.sair")
        await self.load_extension("cogs.tomate")
        await self.load_extension("cogs.status")
        await self.load_extension("cogs.cargo")
        await self.load_extension("cogs.primeiradama")
        await self.load_extension("cogs.tellonym")
        await self.load_extension("cogs.avaliar")

        # 🔁 Slash commands
        # TESTE → sempre
        await self.tree.sync(guild=discord.Object(id=TEST_GUILD_ID))

        # PRODUÇÃO → só se quiser (comentado por padrão)
        # await self.tree.sync(guild=discord.Object(id=PROD_GUILD_ID))

        print("Slash sync OK (teste ativo, prod seguro)")

    async def on_ready(self):
        print(f"Conectado como {self.user}")
        print("Bot pronto nos dois servidores 🚀")

# ========================
# 🚀 START
# ========================
bot = DualGuildBot()
bot.run(TOKEN)
