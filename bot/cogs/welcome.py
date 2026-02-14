import discord
from discord.ext import commands

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        CHANNEL_ID = 1410053387558322297  # coloca o ID do canal aqui

        channel = member.guild.get_channel(CHANNEL_ID)
        if not channel:
            return

        await channel.send(f"{member.mention} entrou no servidor!\n\n -# <@&1420778000504324238>")

async def setup(bot):
    await bot.add_cog(Welcome(bot))
