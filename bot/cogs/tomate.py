import random
from discord.ext import commands

class Tomate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="tomate",
        description="O bot taca tomate em UMA das 5 mensagens mais recentes"
    )
    @commands.has_permissions(add_reactions=True)
    async def tomate(self, ctx: commands.Context):
        canal = ctx.channel
        emoji = "🍅"

        # pega as últimas 5 mensagens, ignorando a do comando
        mensagens = [
            msg async for msg in canal.history(limit=6)
            if msg.id != ctx.message.id
        ]

        if not mensagens:
            await ctx.send("Não achei nenhuma mensagem pra tacar tomate.")
            return

        mensagem_escolhida = random.choice(mensagens[:5])

        try:
            await mensagem_escolhida.add_reaction(emoji)
            await ctx.send("Tomate lançado!")
        except:
            await ctx.send("Não consegui tacar o tomate.")

async def setup(bot):
    await bot.add_cog(Tomate(bot))
