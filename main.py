import asyncio
import os
import sys
import traceback
from pathlib import Path
from threading import Thread

import discord
from discord.ext import commands
from flask import Flask
from dotenv import load_dotenv


# ============================================================
# CONFIGURAÇÕES
# ============================================================

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN", "").strip()
PORT = int(os.getenv("PORT", "8080"))

BASE_DIR = Path(__file__).resolve().parent
COGS_DIR = BASE_DIR / "cogs"


# ============================================================
# VALIDAÇÃO
# ============================================================

if not TOKEN:
    print("❌ ERRO: DISCORD_TOKEN não encontrado!")
    print("Configure a variável DISCORD_TOKEN no Render.")
    sys.exit(1)


# ============================================================
# FLASK
# ============================================================

app = Flask(__name__)


@app.route("/")
def health_check():
    return {"status": "Bot Celestia is running"}, 200


@app.route("/health")
def health():
    return {"status": "ok"}, 200


# ============================================================
# INTENTS
# ============================================================

intents = discord.Intents.default()
intents.message_content = True


# ============================================================
# BOT
# ============================================================

class CelestiaBot(commands.Bot):

    def __init__(self):
        super().__init__(
            command_prefix=["c."],
            intents=intents,
            help_command=None,
        )

    # ========================================================
    # SETUP HOOK
    # ========================================================

    async def setup_hook(self):

        print("=" * 60, flush=True)
        print("🔧 setup_hook iniciado.", flush=True)
        print("=" * 60, flush=True)

        # Primeiro carrega todas as Cogs
        await self.load_all_cogs()

        # Depois sincroniza os slash commands
        await self.sync_slash_commands()


    # ========================================================
    # CARREGAR COGS
    # ========================================================

    async def load_all_cogs(self):

        print(
            f"📁 Procurando Cogs em: {COGS_DIR}",
            flush=True,
        )

        print(
            f"📁 Pasta existe: {COGS_DIR.is_dir()}",
            flush=True,
        )

        if not COGS_DIR.is_dir():

            print(
                "❌ A pasta 'cogs' não foi encontrada!",
                flush=True,
            )

            return

        cog_files = sorted(
            file
            for file in COGS_DIR.iterdir()
            if file.is_file()
            and file.suffix == ".py"
            and not file.name.startswith("__")
        )

        if not cog_files:

            print(
                "⚠️ Nenhum arquivo Python foi encontrado "
                "na pasta cogs.",
                flush=True,
            )

            return

        print(
            "📄 Cogs encontradas: "
            + ", ".join(file.name for file in cog_files),
            flush=True,
        )

        print("-" * 60, flush=True)

        loaded_count = 0
        failed_count = 0

        for file in cog_files:

            extension_name = f"cogs.{file.stem}"

            try:

                print(
                    f"🔄 Carregando {extension_name}...",
                    flush=True,
                )

                await self.load_extension(extension_name)

                loaded_count += 1

                print(
                    f"✅ Cog carregada: {extension_name}",
                    flush=True,
                )

            except commands.ExtensionAlreadyLoaded:

                print(
                    f"⚠️ Cog já estava carregada: "
                    f"{extension_name}",
                    flush=True,
                )

            except commands.NoEntryPointError:

                failed_count += 1

                print(
                    f"❌ {extension_name} não possui "
                    "`async def setup(bot)`.",
                    flush=True,
                )

            except commands.ExtensionFailed as error:

                failed_count += 1

                original_error = error.original

                print(
                    f"❌ Erro dentro da Cog "
                    f"{extension_name}: "
                    f"{type(original_error).__name__}: "
                    f"{original_error}",
                    flush=True,
                )

                traceback.print_exception(
                    type(original_error),
                    original_error,
                    original_error.__traceback__,
                )

            except Exception as error:

                failed_count += 1

                print(
                    f"❌ Erro ao carregar "
                    f"{extension_name}: "
                    f"{type(error).__name__}: "
                    f"{error}",
                    flush=True,
                )

                traceback.print_exc()

        print("-" * 60, flush=True)

        print(
            f"📦 Resultado: "
            f"{loaded_count} carregadas e "
            f"{failed_count} com erro.",
            flush=True,
        )

        print(
            f"📦 Cogs ativas: "
            f"{list(self.cogs.keys())}",
            flush=True,
        )

        print("-" * 60, flush=True)


    # ========================================================
    # SINCRONIZAR SLASH COMMANDS
    # ========================================================

    async def sync_slash_commands(self):

        try:

            print(
                "🔄 Sincronizando slash commands...",
                flush=True,
            )

            # Mostra os comandos que existem ANTES do sync
            commands_before_sync = self.tree.get_commands()

            print(
                f"📋 Comandos encontrados na árvore: "
                f"{len(commands_before_sync)}",
                flush=True,
            )

            if commands_before_sync:

                for command in commands_before_sync:

                    print(
                        f"   → /{command.name}",
                        flush=True,
                    )

            else:

                print(
                    "⚠️ Nenhum slash command foi registrado "
                    "na árvore do bot.",
                    flush=True,
                )

            # Sincronização GLOBAL
            synced = await self.tree.sync()

            print(
                f"✅ {len(synced)} slash command(s) "
                f"sincronizado(s) globalmente!",
                flush=True,
            )

            if synced:

                print(
                    "📋 Comandos sincronizados:",
                    flush=True,
                )

                for command in synced:

                    print(
                        f"   → /{command.name}",
                        flush=True,
                    )

            else:

                print(
                    "⚠️ O Discord retornou 0 comandos.",
                    flush=True,
                )

        except discord.Forbidden as error:

            print(
                "❌ O Discord negou a sincronização.",
                flush=True,
            )

            print(
                "Verifique se o bot foi convidado "
                "com o scope applications.commands.",
                flush=True,
            )

            print(
                f"Detalhes: {error}",
                flush=True,
            )

        except discord.HTTPException as error:

            print(
                f"❌ Erro HTTP ao sincronizar comandos: "
                f"{error}",
                flush=True,
            )

        except Exception as error:

            print(
                f"❌ Erro inesperado ao sincronizar: "
                f"{type(error).__name__}: {error}",
                flush=True,
            )

            traceback.print_exc()


# ============================================================
# INSTÂNCIA DO BOT
# ============================================================

bot = CelestiaBot()


# ============================================================
# EVENTO ON_READY
# ============================================================

@bot.event
async def on_ready():

    if bot.user is None:
        return

    print("=" * 60, flush=True)

    print(
        f"✅ Logado como {bot.user} | "
        f"ID: {bot.user.id}",
        flush=True,
    )

    print(
        f"🌐 Conectado em {len(bot.guilds)} servidor(es).",
        flush=True,
    )

    print(
        f"📦 Cogs carregadas: {len(bot.cogs)}",
        flush=True,
    )

    print(
        f"⚡ Latência: "
        f"{round(bot.latency * 1000)} ms",
        flush=True,
    )

    print("=" * 60, flush=True)


# ============================================================
# FLASK
# ============================================================

def run_flask():

    print(
        f"🚀 Servidor web rodando na porta {PORT}",
        flush=True,
    )

    app.run(
        host="0.0.0.0",
        port=PORT,
        debug=False,
    )


# ============================================================
# MAIN
# ============================================================

async def main():

    print(
        "🚀 Inicializando Bot Celestia...",
        flush=True,
    )

    print(
        f"📁 Diretório principal: {BASE_DIR}",
        flush=True,
    )

    print(
        f"📁 Diretório das Cogs: {COGS_DIR}",
        flush=True,
    )

    # Inicia Flask
    flask_thread = Thread(
        target=run_flask,
        daemon=True,
    )

    flask_thread.start()

    print(
        "🤖 Iniciando conexão com o Discord...",
        flush=True,
    )

    try:

        async with bot:

            await bot.start(TOKEN)

    except discord.LoginFailure as error:

        print(
            "❌ O Discord recusou o token do bot.",
            flush=True,
        )

        raise error

    except discord.PrivilegedIntentsRequired as error:

        print(
            "❌ Existem Intents privilegiados "
            "que precisam ser ativados no "
            "Discord Developer Portal.",
            flush=True,
        )

        raise error

    except Exception as error:

        print(
            f"❌ Erro fatal ao iniciar o bot: "
            f"{type(error).__name__}: {error}",
            flush=True,
        )

        traceback.print_exc()

        raise


# ============================================================
# EXECUTAR
# ============================================================

if __name__ == "__main__":

    try:

        asyncio.run(main())

    except KeyboardInterrupt:

        print(
            "\n⏹️ Bot Celestia encerrado pelo usuário.",
            flush=True,
        )

    except Exception as error:

        print(
            f"💥 O processo foi encerrado: "
            f"{type(error).__name__}: {error}",
            flush=True,
        )
