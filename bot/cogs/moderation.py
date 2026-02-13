import discord
from discord import app_commands
from discord.ext import commands
from datetime import timedelta
import asyncio
from bot.db import get_conn


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 🔒 Checagem global (admin)
    async def cog_check(self, ctx: commands.Context):
        return ctx.author.guild_permissions.administrator

    # =====================
    # 🔨 BAN
    # =====================
    @commands.hybrid_command(
        name="ban",
        description="Banir um usuário com tempo opcional",
    )
    @app_commands.describe(
        user="Usuário",
        time="Duração em segundos",
        reason="Motivo",
    )
    @commands.has_permissions(ban_members=True)
    async def ban(
        self,
        ctx: commands.Context,
        user: discord.Member,
        time: int | None = None,
        *,
        reason: str = "Nenhum motivo fornecido.",
    ):
        await user.ban(reason=reason)

        embed = discord.Embed(
            title="Usuário banido",
            color=discord.Color.red(),
        )
        embed.add_field(
            name="Usuário",
            value=f"{user} ({user.id})",
            inline=False,
        )
        embed.add_field(
            name="Admin",
            value=f"{ctx.author} ({ctx.author.id})",
            inline=False,
        )
        embed.add_field(
            name="Motivo",
            value=reason,
            inline=False,
        )

        if time:
            embed.add_field(
                name="Duração",
                value=f"{time} segundos",
                inline=False,
            )

        await ctx.send(embed=embed)

        # ⏰ Desban automático
        if time:
            await asyncio.sleep(time)
            await ctx.guild.unban(user)
            await ctx.send(
                f"**{user.name}** foi desbanido após **{time} segundos**."
            )

    # =====================
    # 👢 KICK
    # =====================
    @commands.hybrid_command(
        name="kick",
        description="Expulsar um usuário",
    )
    @app_commands.describe(
        user="Usuário",
        reason="Motivo",
    )
    @commands.has_permissions(kick_members=True)
    async def kick(
        self,
        ctx: commands.Context,
        user: discord.Member,
        *,
        reason: str = "Nenhum motivo fornecido.",
    ):
        await user.kick(reason=reason)
        await ctx.send(
            f"**{user.name}** foi expulso. Motivo: {reason}"
        )

    # =====================
    # 🔇 MUTE / TIMEOUT
    # =====================
    @commands.hybrid_command(
        name="mute",
        description="Silenciar um usuário",
    )
    @app_commands.describe(
        user="Usuário",
        time="Duração em minutos",
        reason="Motivo",
    )
    @commands.has_permissions(moderate_members=True)
    async def mute(
        self,
        ctx: commands.Context,
        user: discord.Member,
        time: int,
        *,
        reason: str = "Nenhum motivo fornecido.",
    ):
        duration = timedelta(minutes=time)
        await user.timeout(duration, reason=reason)

        await ctx.send(
            f"**{user.name}** foi silenciado por **{time} minutos**! Motivo: {reason}."
        )

    # =====================
    # ⚠️ WARN
    # =====================
    @commands.hybrid_command(
        name="warn",
        description="Avisar um usuário",
    )
    @app_commands.describe(
        user="Usuário",
        reason="Motivo",
    )
    @commands.has_permissions(manage_messages=True)
    async def warn(
        self,
        ctx: commands.Context,
        user: discord.Member,
        *,
        reason: str = "Nenhum motivo fornecido.",
    ):
        try:
            conn = get_conn()
            cur = conn.cursor()

            cur.execute(
                "INSERT INTO warns (user_id, moderator_id, reason) VALUES (%s, %s, %s)",
                (str(user.id), str(ctx.author.id), reason),
            )
            conn.commit()

        finally:
            cur.close()
            conn.close()

        await ctx.send(
            f"O usuário **{user.name}** recebeu um warn! Motivo: {reason}"
        )


async def setup(bot):
    await bot.add_cog(Moderation(bot))
