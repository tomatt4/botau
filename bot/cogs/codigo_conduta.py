import discord
from discord.ext import commands

class CodigoConduta(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="sobre", aliases=["codigodeconduta", "staffconduta"])
    @commands.has_permissions(administrator=True)
    async def codigo_conduta(self, ctx):
        embed = discord.Embed(
            title="Poxa...",
            description=(
                "Infelizmente a loja está fechada por causa da falta de boosts! Poderia impulsionar para ajudar o servidor?"
            ),
            color=discord.Color.from_rgb(255, 255, 255)
        )

        embed.set_footer(text="A loja será aberta quando tiver boosts suficientes!")
        embed.set_image(url="")

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(CodigoConduta(bot))