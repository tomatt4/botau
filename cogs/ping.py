import discord
from discord.ext import commands

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="ping", description="Verifica a latência do bot")
    async def ping(self, interaction: discord.Interaction):
        """Comando que retorna o ping do bot - Suporta /ping e c.ping"""
        latency = round(self.bot.latency * 1000)
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"Latência: **{latency}ms**",
            color=discord.Color.blue()
        )
        await interaction.response.send_message(embed=embed)
    
    # Versão com prefixo de texto para "c.ping"
    @commands.command(name="ping")
    async def ping_prefix(self, ctx):
        """Comando com prefixo - c.ping"""
        latency = round(self.bot.latency * 1000)
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"Latência: **{latency}ms**",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Ping(bot))
