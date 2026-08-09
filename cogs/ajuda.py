import discord
from discord.ext import commands

class Ajuda(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="ajuda", description="Exibe a lista de comandos disponíveis")
    async def ajuda(self, interaction: discord.Interaction):
        """Comando que mostra a ajuda do bot - Suporta /ajuda e c.ajuda"""
        embed = discord.Embed(
            title="📚 Ajuda do Celestia",
            description="Aqui estão todos os comandos disponíveis:\n\n**Você pode usar `/comando` ou `c.comando`**",
            color=discord.Color.purple()
        )
        
        embed.add_field(
            name="/ping ou c.ping",
            value="Verifica a latência do bot",
            inline=False
        )
        
        embed.add_field(
            name="/ajuda ou c.ajuda",
            value="Exibe esta mensagem de ajuda",
            inline=False
        )
        
        embed.add_field(
            name="/averiguar resenha",
            value="Averigua se há uma resenha disponível (sem prefixo alternativo)",
            inline=False
        )
        
        embed.set_footer(text="Celestia Bot v1.1 - Sincronizado com prefixo 'c.'")
        
        await interaction.response.send_message(embed=embed)
    
    # Versão com prefixo de texto para "c.ajuda"
    @commands.command(name="ajuda")
    async def ajuda_prefix(self, ctx):
        """Comando com prefixo - c.ajuda"""
        embed = discord.Embed(
            title="📚 Ajuda do Celestia",
            description="Aqui estão todos os comandos disponíveis:\n\n**Você pode usar `/comando` ou `c.comando`**",
            color=discord.Color.purple()
        )
        
        embed.add_field(
            name="/ping ou c.ping",
            value="Verifica a latência do bot",
            inline=False
        )
        
        embed.add_field(
            name="/ajuda ou c.ajuda",
            value="Exibe esta mensagem de ajuda",
            inline=False
        )
        
        embed.add_field(
            name="/averiguar resenha",
            value="Averigua se há uma resenha disponível (sem prefixo alternativo)",
            inline=False
        )
        
        embed.set_footer(text="Celestia Bot v1.1 - Sincronizado com prefixo 'c.'")
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Ajuda(bot))
