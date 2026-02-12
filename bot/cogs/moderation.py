import discord
from discord import app_commands
from discord.ext import commands
from datetime import timedelta
import asyncio
from bot.db import get_conn


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return ctx.author.guild_permissions.administrator

    @commands.hybrid_command(name="ban", description="Banir um usuário com um tempo")
    @app_commands.describe(user="Usuários", time="Duração em segundos", reason="Motivo")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.Member, time: int = None, *, reason: str = "Nenhum motivo fornecido."):
        await user.ban(reason=reason)
        
        embed = discord.Embed(title="Usuário banido")
        embed.add_field(name="<:members:1457446686774526094> | Usuário", value=f"{user.name} ({user.id})", inline=False)
        embed.add_field(name="<:admin:1457446645015773426> | Admin", value=ctx.author.name, inline=False)
        embed.add_field(name="<:FAQ:1457446924842963006> | Motivo", value=reason, inline=False)
        if time:
            embed.add_field(name="Duração", value=f"{time} segundos", inline=False)
        
        await ctx.send(embed=embed)

        if time:
            await asyncio.sleep(time)
            await ctx.guild.unban(user)
            await ctx.send(f"{user.name} foi desbanido depois de {time} segundos.")

    @commands.hybrid_command(name="kick", description="Expulse um usuário")
    @app_commands.describe(user="Usuário", reason="Motivo")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.Member, *, reason: str = "Nenhum motivo fornecido."):
        await user.kick(reason=reason)
        await ctx.send(f"Expulsado {user.name}. Motivo: {reason}")

    @commands.hybrid_command(name="mute", description="Silenciar um usuário")
    @app_commands.describe(user="Usuário", time="Duração em minutos", reason="Motivo")
    @commands.has_permissions(moderate_members=True)
    async def silenciar(self, ctx, user: discord.Member, time: int, *, reason: str = "Nenhnum motivo fornecido."):
        duration = timedelta(minutes=time)
        await user.timeout(duration, reason=reason)
        await ctx.send(f"{user.name} foi silenciado por {time} minutos. Motivo: {reason}")

    @commands.hybrid_command(name="warn", description="Avisar um usuário")
    @app_commands.describe(user="Usuário", reason="Motivo")
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, user: discord.Member, *, reason: str = "Nenhum motivo fornecido."):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO warns (user_id, moderator_id, reason) VALUES (%s, %s, %s)", 
                    (str(user.id), str(ctx.author.id), reason))
        conn.commit()
        cur.close()
        conn.close()
        await ctx.send(f"Membro avisado: {user.name}. Motivo: {reason}")

async def setup(bot):
    await bot.add_cog(Moderation(bot))
