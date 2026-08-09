import discord
from discord.ext import commands

class Ajuda(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="ajuda", description="Exibe a lista de comandos disponíveis")
    async def ajuda(self, interaction: discord.Interaction):
        """Comando que mostra a ajuda do bot"""
        embed = discord.Embed(
            title="📚 Ajuda do Celestia",
            description="Aqui estão todos os comandos disponíveis:",
            color=discord.Color.purple()
        )
        
        embed.add_field(
            name="/ping",
            value="Verifica a latência do bot",
            inline=False
        )
        
        embed.add_field(
            name="/ajuda",
            value="Exibe esta mensagem de ajuda",
            inline=False
        )
        
        embed.set_footer(text="Celestia Bot v1.0")
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Ajuda(bot))