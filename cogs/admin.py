from datetime import timedelta
import discord
from discord.ext import commands


class Moderacao(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  # ==========================================
  # COMANDO DE KICK (Expulsar)
  # ==========================================
  @commands.command(name="kick", help="Expulsa um usuário do servidor.")
  @commands.has_permissions(kick_members=True)
  async def kick(self, ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(
        f"✅ {member.mention} foi expulso do servidor. Motivo: {reason}"
    )

  @kick.error
  async def kick_error(self, ctx, error):
    if isinstance(error, commands.MissingPermissions):
      await ctx.send("❌ Você não tem permissão para usar este comando.")
    elif isinstance(error, commands.MissingRequiredArgument):
      await ctx.send(
          "❌ Você precisa mencionar um usuário. Exemplo: `!kick @usuario"
          " motivo`"
      )

  # ==========================================
  # COMANDO DE BAN (Banir)
  # ==========================================
  @commands.command(name="ban", help="Bane um usuário do servidor.")
  @commands.has_permissions(ban_members=True)
  async def ban(self, ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(
        f"✅ {member.mention} foi banido do servidor. Motivo: {reason}"
    )

  @ban.error
  async def ban_error(self, ctx, error):
    if isinstance(error, commands.MissingPermissions):
      await ctx.send("❌ Você não tem permissão para usar este comando.")
    elif isinstance(error, commands.MissingRequiredArgument):
      await ctx.send(
          "❌ Você precisa mencionar um usuário. Exemplo: `!ban @usuario"
          " motivo`"
      )

  # ==========================================
  # COMANDO DE MUTE (Timeout / Castigo)
  # ==========================================
  @commands.command(
      name="mute", help="Silencia um usuário temporariamente (Timeout)."
  )
  @commands.has_permissions(moderate_members=True)
  async def mute(
      self, ctx, member: discord.Member, minutes: int, *, reason=None
  ):
    duration = timedelta(minutes=minutes)
    await member.timeout(duration, reason=reason)
    await ctx.send(
        f"✅ {member.mention} foi silenciado por {minutes} minuto(s). Motivo:"
        f" {reason}"
    )

  @mute.error
  async def mute_error(self, ctx, error):
    if isinstance(error, commands.MissingPermissions):
      await ctx.send("❌ Você não tem permissão para usar este comando.")
    elif isinstance(error, commands.MissingRequiredArgument):
      await ctx.send(
          "❌ Uso correto: `c.mute @usuario [minutos] [motivo]`"
      )


async def setup(bot):
  await bot.add_cog(Moderacao(bot))
