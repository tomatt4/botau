import discord
from discord.ext import commands
import os
import sys
from flask import Flask
from threading import Thread
import asyncio

# Carregar variáveis de ambiente
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("python-dotenv não instalado. Usando variáveis de ambiente do sistema.")

TOKEN = os.getenv("DISCORD_TOKEN")
PORT = int(os.getenv("PORT", 8080))

if not TOKEN:
    print("❌ ERRO: DISCORD_TOKEN não encontrado nas variáveis de ambiente!")
    print("Configure o token no arquivo .env ou na variável de ambiente DISCORD_TOKEN")
    sys.exit(1)

# Criar app Flask para manter o serviço ativo no Render
app = Flask(__name__)

@app.route('/')
def health_check():
    return {'status': 'Bot Celestia is running'}, 200

@app.route('/health')
def health():
    return {'status': 'ok'}, 200
    
# Configuração do bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

# Evento: Bot conectado
@bot.event
async def on_ready():
    print(f"✅ {bot.user} está online!")
    try:
        synced = await bot.tree.sync()
        print(f"✅ {len(synced)} comando(s) sincronizado(s)")
    except Exception as e:
        print(f"❌ Erro ao sincronizar comandos: {e}")

# Carregar cogs
async def load_cogs():
    cogs_dir = "./cogs"
    if not os.path.exists(cogs_dir):
        print(f"⚠️  Pasta {cogs_dir} não encontrada!")
        return
    
    for filename in os.listdir(cogs_dir):
        if filename.endswith(".py") and not filename.startswith("_"):
            try:
                await bot.load_extension(f"cogs.{filename[:-3]}")
                print(f"✅ Cog carregada: {filename}")
            except Exception as e:
                print(f"❌ Erro ao carregar {filename}: {e}")

# Função para executar o bot
async def main():
    async with bot:
        await load_cogs()
        try:
            await bot.start(TOKEN)
        except discord.errors.LoginFailure:
            print("❌ ERRO: Token inválido!")
            sys.exit(1)
        except Exception as e:
            print(f"❌ ERRO ao iniciar bot: {e}")
            sys.exit(1)

def run_flask():
    """Executa o servidor Flask em thread separada"""
    print(f"🚀 Servidor web rodando na porta {PORT}")
    app.run(host='0.0.0.0', port=PORT, debug=False)

if __name__ == "__main__":
    # Inicia Flask em uma thread separada
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # Inicia o bot Discord na thread principal
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⏹️  Bot desligado pelo usuário")
    except Exception as e:
        print(f"❌ Erro fatal: {e}")
        sys.exit(1)
