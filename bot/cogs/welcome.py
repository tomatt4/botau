import discord
from discord.ext import commands

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        CHANNEL_ID = 1410053387558322297

        channel = member.guild.get_channel(CHANNEL_ID)
        if not channel:
            return

        await channel.send(f"**Boas vindas à Spider Hub {member.mention}!**\n\n- **Quer mostrar que time você é? Vá em <#1450943288533323879>!**\n\n- **Ficou interessado em um VIP? Veja os preços na categoria 𝐋𝐨𝐣𝐚!**\n\n-# <@&1420778000504324238>")

async def setup(bot):
    await bot.add_cog(Welcome(bot))
