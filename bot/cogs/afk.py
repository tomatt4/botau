import discord
from discord.ext import commands

class AFK(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.afk_users = {}  # user_id: motivo

    @commands.hybrid_command(name="afk", description="Ficar AFK")
    async def afk(self, ctx: commands.Context, *, motivo: str = "AFK"):
        self.afk_users[ctx.author.id] = motivo
        await ctx.send(f"Seu afk foi setado como ***{motivo}***. Até mais!")

    @commands.Cog.listener()
async def on_message(self, message: discord.Message):
    if message.author.bot:
        return

    # Remove AFK ao falar
    if message.author.id in self.afk_users:
        del self.afk_users[message.author.id]

    if message.mention_everyone:
        return

    afk_detected = set()

    # Menções diretas
    for user in message.mentions:
        if user.id in self.afk_users:
            afk_detected.add(user)

    # Reply
    if message.reference:
        try:
            replied_msg = await message.channel.fetch_message(
                message.reference.message_id
            )
            if replied_msg.author.id in self.afk_users:
                afk_detected.add(replied_msg.author)
        except discord.NotFound:
            pass

    for user in afk_detected:
        motivo = self.afk_users[user.id]
        await message.channel.send(
            f"**{user.display_name}** está afk! Motivo: **{motivo}**"
        )

    # MUITO IMPORTANTE
    await self.bot.process_commands(message)

async def setup(bot):
 await bot.add_cog(AFK(bot))
