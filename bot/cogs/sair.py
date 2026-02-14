import random
from discord.ext import commands

class Kitar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="kitar",
        description="Kita do servidor (mentira) com uma frase engraçada"
    )
    async def kitar(self, ctx: commands.Context):
        membro = ctx.author

        frases = [
            f"{membro.mention} kitou porque foi cancelado pelo Elon Musk",
            f"{membro.mention} kitou pra tocar grama",
            f"{membro.mention} kitou após descobrir o ping negativo",
            f"{membro.mention} kitou pra virar NPC do TikTok",
            f"{membro.mention} kitou porque confundiu Discord com WhatsApp",
            f"{membro.mention} kitou dizendo 'já volto' (não voltou)",
            f"{membro.mention} kitou pra buscar o leite",
            f"{membro.mention} kitou da realidade",
            f"{membro.mention} kitou porque o bot mandou",
        ]

        await ctx.send(random.choice(frases))

async def setup(bot):
    await bot.add_cog(Kitar(bot))
