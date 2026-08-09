# Celestia Bot

Um bot Discord moderno e bem organizado chamado **Celestia**, com comandos separados em cogs.

## 🚀 Estrutura do Projeto

```
botau/
├── main.py              # Arquivo principal do bot
├── requirements.txt     # Dependências do projeto
├── .env.example        # Exemplo de variáveis de ambiente
├── cogs/               # Pasta com todos os comandos
│   ├── ping.py         # Comando /ping
│   └── ajuda.py        # Comando /ajuda
└── README.md           # Este arquivo
```

## 📋 Requisitos

- Python 3.8+
- Discord.py 2.3.2+

## 🔧 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/tomatt4/botau.git
cd botau
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure o token do Discord:
   - Copie `.env.example` para `.env`
   - Substitua `INSIRA_SEU_TOKEN_AQUI` pelo seu token real

4. Execute o bot:
```bash
python main.py
```

## 📝 Comandos Disponíveis

### `/ping`
Verifica a latência do bot em milissegundos.

**Uso:** `/ping`

### `/ajuda`
Exibe a lista de todos os comandos disponíveis.

**Uso:** `/ajuda`

## 📚 Adicionando Novos Comandos

1. Crie um novo arquivo em `cogs/` com o nome do comando
2. Implemente a classe Cog do discord.py
3. O arquivo será carregado automaticamente ao iniciar o bot

Exemplo:
```python
import discord
from discord.ext import commands

class MeuComando(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="meucomando", description="Descrição")
    async def meucomando(self, interaction: discord.Interaction):
        await interaction.response.send_message("Hello!")

async def setup(bot):
    await bot.add_cog(MeuComando(bot))
```

## 🔐 Segurança

- **Nunca** compartilhe seu token do Discord
- Use o arquivo `.env` para armazenar seu token
- Adicione `.env` ao `.gitignore`

## 📧 Suporte

Para dúvidas ou problemas, abra uma issue no repositório.

---

**Celestia Bot v1.0** 🌟