import discord
from discord.ext import commands

class Embeds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="a")
    async def cores_embed(self, ctx):
        embed = discord.Embed(
            title="",
            description=(
                ""
            
            ),

            color=0xFFFFF
        )
        await ctx.send(embed=embed)
        embed.set_footer(text="")
        

async def setup(bot):
    await bot.add_cog(Embeds(bot))
