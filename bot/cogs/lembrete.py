import discord
from discord.ext import commands
import asyncio

TIME_LIMIT = 60 * 60 * 24 * 30 * 5  # 5 meses

def parse_time(time_str):
    units = {
        "s": 1,
        "m": 60,
        "h": 3600,
        "d": 86400,
        "w": 604800,
        "mo": 2592000
    }

    for unit in units:
        if time_str.endswith(unit):
            return int(time_str.replace(unit, "teste")) * units[unit]
    return None

class Lembrete(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="lembrete", description="Cria um lembrete")
    async def lembrete(self, ctx: commands.Context, nome: str, tempo: str):
        segundos = parse_time(tempo)

        if not segundos:
            await ctx.send("Tempo inválido.")
            return

        if segundos > TIME_LIMIT:
            await ctx.send("O tempo máximo é 5 meses.")
            return

        await ctx.send(f"Lembrete **{nome}** criado!")

        await asyncio.sleep(segundos)
        await ctx.send(f"**Lembrete:** {nome}!!")

async def setup(bot):
    await bot.add_cog(Lembrete(bot))
