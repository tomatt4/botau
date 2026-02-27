import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

# ========================
# 🔐 ENV
# ========================
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
TEST_GUILD_ID = int(os.getenv("TEST_GUILD_ID"))  # servidor de teste
PROD_GUILD_ID = int(os.getenv("PROD_GUILD_ID"))  # servidor oficial

if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN não encontrado no .env")

# ========================
# 🧠 INTENTS (mínimos e seguros)
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
            activity=discord.Game(name="COÉ DISCORD FUI BANIDO DA API")
        )

    async def setup_hook(self):
        # ========================
        # 📦 LOAD SEGURO DOS COGS
        # ========================
        cogs = [
            "cogs.welcome",
            "cogs.random_number"
            # adiciona aqui só os essenciais
        ]

        for ext in cogs:
            try:
                await self.load_extension(ext)
                print(f"[OK] {ext}")
            except Exception as e:
                print(f"[ERRO] {ext} → {e}")

        # ========================
        # 🎫 VIEW PERSISTENTE
        # ========================
        try:
            from cogs.tickets import TicketView
            self.add_view(TicketView())
            print("[OK] TicketView persistente registrada")
        except Exception as e:
            print(f"[ERRO] TicketView → {e}")

        # ========================
        # 🔁 SLASH COMMANDS
        # ========================
        # 🧪 TESTE → sempre
        await self.tree.sync(guild=discord.Object(id=TEST_GUILD_ID))
        print("[OK] Slash sync no servidor de TESTE")

        # 🏭 PRODUÇÃO → só quando mudar comandos
        # await self.tree.sync(guild=discord.Object(id=PROD_GUILD_ID))

    async def on_ready(self):
        print(f"Conectado como {self.user}")
        print("Bot pronto 🚀")

# ========================
# 🚀 START
# ========================
bot = DualGuildBot()
bot.run(TOKEN)
