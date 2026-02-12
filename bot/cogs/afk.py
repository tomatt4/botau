import discord
from discord.ext import commands

class AFK(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.afk_users = {}  # user_id: motivo

    @commands.hybrid_command(name="afk", description="Ficar AFK")
    async def afk(self, ctx: commands.Context, *, motivo: str = "AFK"):
        self.afk_users[ctx.author.id] = motivo
        await ctx.send(f"🌙 {ctx.author.mention} agora está AFK: **{motivo}**")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        # 🔹 Se o autor estava AFK, remove silenciosamente
        if message.author.id in self.afk_users:
            del self.afk_users[message.author.id]

        # 🔹 Se mencionar alguém AFK (Diretamente ou via Resposta)
        # Ignora menções de everyone, here ou cargos
        if message.mention_everyone:
            return

        afk_detected = set()

        # 1. Menções diretas no conteúdo da mensagem (excluindo cargos)
        for user in message.mentions:
            if user.id in self.afk_users:
                afk_detected.add(user)

        # 2. Usuário que está sendo respondido (Reply)
        if message.reference and message.reference.resolved:
            replied_msg = message.reference.resolved
            if isinstance(replied_msg, discord.Message):
                replied_user = replied_msg.author
                if replied_user.id in self.afk_users:
                    afk_detected.add(replied_user)

        # Avisa para os usuários detectados
        for user in afk_detected:
            motivo = self.afk_users[user.id]
            await message.channel.send(
                f"{user.display_name} está AFK. **{motivo}**"
            )
async def setup(bot):
 await bot.add_cog(AFK(bot))