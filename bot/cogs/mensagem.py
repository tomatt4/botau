from discord.ext import commands

class mensagem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="")
    async def mensagem(self, ctx):
        await ctx.send("")

async def setup(bot):
    await bot.add_cog(mensagem(bot))