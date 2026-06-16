import discord
from discord import app_commands
from discord.ext import commands

from utils.ai_client import gerar_resposta


class IA(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="ia",
        description="Converse com o Hakari."
    )
    @app_commands.describe(
        mensagem="O que você quer perguntar para o Hakari?"
    )
    async def ia(self, interaction: discord.Interaction, mensagem: str):
        await interaction.response.defer(thinking=True)

        resposta = await gerar_resposta(
            mensagem=mensagem,
            usuario=str(interaction.user)
        )

        if len(resposta) > 1900:
            resposta = resposta[:1900] + "\n\n⚠️ Resposta cortada porque passou do limite do Discord."

        await interaction.followup.send(resposta)


async def setup(bot):
    await bot.add_cog(IA(bot))
