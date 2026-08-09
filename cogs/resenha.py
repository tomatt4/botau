import discord
from discord.ext import commands
from discord import app_commands
import random
import asyncio


class Procurar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="averiguar resenha",
        description="Computador, ligue máquina de averiguar resenha, e averigue possível resenha"
    )
    async def procurar(self, interaction: discord.Interaction):
        """Comando que averigua resenha - Apenas com /averiguar resenha (sem prefixo alternativo)"""

        # Primeiro responde "Procurando..."
        await interaction.response.send_message("<a:carregarAnimado:1536097479840505997> Averiguando resenha...")

        # Espera 5 segundos
        await asyncio.sleep(5)

        # Escolhe aleatoriamente o resultado
        respostas = [
            "✅ Resenha confirmada.",
            "❌ Resenha tá fraca hoje."
        ]

        resposta = random.choice(respostas)

        # Edita a mensagem anterior
        await interaction.edit_original_response(
            content=resposta
        )


async def setup(bot):
    await bot.add_cog(Procurar(bot))
