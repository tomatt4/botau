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
            f"{membro.mention} kitou porque é um favelado subdesenvolvido(homenagem ao bleki)",
            f"{membro.mention} kitou porque é um beta",
            f"{membro.mention} kitou pra fazer live NPC do TikTok",
            f"{membro.mention} kitou porque confundiu Discord com WhatsApp",
            f"{membro.mention} kitou dizendo 'já volto' (obs: não voltou)",
            f"{membro.mention} kitou porque foi ali fumar cigarro",
            f"{membro.mention} kitou da realidade",
            f"{membro.mention} kitou porque o bot mandou",
            f"{membro.mention} kitou porque o Cristiano Ronaldo recusou o pedido de casamento",
            f"{membro.mention} kitou porque o Neymar traiu ele",
        ]

        await ctx.send(random.choice(frases))

async def setup(bot):
    await bot.add_cog(Kitar(bot))
