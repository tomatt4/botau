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
                "# *<@&1469484491767550184>*\n\n"
                "para aqueles que apoiam a comunidade de maneira simples, mas significativa.\n\n"
                "o cargo **Exctinct Archangels** é concedido para quem coloca o link do servidor em sua bio — um gesto discreto, mas poderoso, que mostra que você faz parte da essência do nosso servidor.\n\n"
                "**permissões básicas:**\n"
                "• fotos, e vídeos no chat.\n"
                "• reconhecimento especial entre os membros.\n"
                "• direitos básicos de interação no servidor.\n\n"
                "mesmo com poucas permissões, ser **extinct archangels** é um símbolo de pertencimento e apoio à comunidade. Você já faz parte do grupo que mantém o servidor vivo."
            
            ),

            color=0xFFFFFF
        )
        await ctx.send(embed=embed)
        embed.set_footer(text="")
        

async def setup(bot):
    await bot.add_cog(Embeds(bot))
