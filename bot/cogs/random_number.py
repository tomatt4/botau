import random
from discord.ext import commands

class RandomNumber(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="numero",
        description="Gera um número aleatório entre 1 e 100"
    )
    async def numero(self, ctx: commands.Context):
        numero = random.randint(1, 100)
        await ctx.send(f"Eu escolho... **{numero}**! Caso queira outro número é só rodar esse comando novamente.")

async def setup(bot):
    await bot.add_cog(RandomNumber(bot))
