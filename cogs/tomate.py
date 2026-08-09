import discord
from discord.ext import commands
import random


class Tomate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="tomate")
    async def tomate(self, ctx):
        # Pega as 5 mensagens mais recentes ANTES do comando
        mensagens = []

        async for mensagem in ctx.channel.history(limit=6):
            # Ignora o próprio comando
            if mensagem.id != ctx.message.id:
                mensagens.append(mensagem)

        # Caso tenha menos de 5 mensagens no canal
        if len(mensagens) < 5:
            await ctx.send("🍅 Não tem 5 mensagens recentes pra jogar o tomate!")
            return

        # Escolhe uma das 5 aleatoriamente
        alvo = random.choice(mensagens[:5])

        # Reage com tomate na mensagem escolhida
        await alvo.add_reaction("🍅")

        # Mensagem de efeito
        await ctx.send(
            f"🍅 **{ctx.author.display_name} jogou um tomate em {alvo.author.mention}!**"
        )


async def setup(bot):
    await bot.add_cog(Tomate(bot))
