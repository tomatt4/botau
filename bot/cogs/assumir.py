import discord
from discord.ext import commands
from db import get_conn

class Assumir(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="assumir",
        description="Assumir o ticket atual"
    )
    @commands.has_permissions(administrator=True)
    async def assumir(self, ctx: commands.Context):
        # verifica se é um ticket válido
        conn = get_conn()
        cur = conn.cursor()

        cur.execute(
            "SELECT id FROM tickets WHERE channel_id = %s",
            (str(ctx.channel.id),)
        )
        result = cur.fetchone()

        if not result:
            if ctx.interaction:
                await ctx.interaction.response.send_message(
                    "<:Warning:1457445578593009734> | Amigão... bebeu foi? Esse canal não é um ticket.",
                    ephemeral=True
                )
            else:
                await ctx.send("<:Warning:1457445578593009734> | Amigão... bebeu foi? Esse canal não é um ticket.")
            cur.close()
            conn.close()
            return

        cur.close()
        conn.close()

        mensagem = (
            f"Ticket assumido!"
        )

        # separação correta entre slash e prefixo
        if ctx.interaction:
            await ctx.interaction.response.send_message(mensagem)
        else:
            await ctx.send(mensagem)

async def setup(bot):
    await bot.add_cog(Assumir(bot))
