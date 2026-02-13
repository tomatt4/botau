import discord
from discord.ext import commands
import re

class IPDetection(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ip_pattern = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if self.ip_pattern.search(message.content):
            await message.delete()
            await message.channel.send(f"Vazamento de IP é PROIBIDO.")

async def setup(bot):
    await bot.add_cog(IPDetection(bot))
