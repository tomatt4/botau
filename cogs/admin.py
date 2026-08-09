from datetime import timedelta
import discord
from discord.ext import commands
from discord import app_commands


class Moderacao(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # ==========================================
    # COMANDO DE KICK (Expulsar)
    # ==========================================
    
    # Versão Slash Command
    @app_commands.command(name="kick", description="Expulsa um usuário do servidor.")
    @app_commands.describe(
        member="O membro a ser expulso",
        reason="Motivo da expulsão (opcional)"
    )
    @commands.has_permissions(kick_members=True)
    async def kick_slash(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        """Comando /kick - Expulsa um usuário"""
        try:
            await member.kick(reason=reason)
            embed = discord.Embed(
                title="✅ Membro Expulso",
                description=f"{member.mention} foi expulso do servidor.",
                color=discord.Color.red()
            )
            if reason:
                embed.add_field(name="Motivo", value=reason, inline=False)
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message(f"❌ Erro ao expulsar: {str(e)}", ephemeral=True)

    # Versão com prefixo "c."
    @commands.command(name="kick", help="Expulsa um usuário do servidor.")
    @commands.has_permissions(kick_members=True)
    async def kick_prefix(self, ctx, member: discord.Member, *, reason=None):
        """Comando c.kick - Expulsa um usuário"""
        try:
            await member.kick(reason=reason)
            embed = discord.Embed(
                title="✅ Membro Expulso",
                description=f"{member.mention} foi expulso do servidor.",
                color=discord.Color.red()
            )
            if reason:
                embed.add_field(name="Motivo", value=reason, inline=False)
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"❌ Erro ao expulsar: {str(e)}")

    @kick_prefix.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ Você não tem permissão para usar este comando.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("❌ Você precisa mencionar um usuário. Exemplo: `c.kick @usuario motivo`")

    # ==========================================
    # COMANDO DE BAN (Banir)
    # ==========================================
    
    # Versão Slash Command
    @app_commands.command(name="ban", description="Bane um usuário do servidor.")
    @app_commands.describe(
        member="O membro a ser banido",
        reason="Motivo do banimento (opcional)"
    )
    @commands.has_permissions(ban_members=True)
    async def ban_slash(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        """Comando /ban - Bane um usuário"""
        try:
            await member.ban(reason=reason)
            embed = discord.Embed(
                title="✅ Membro Banido",
                description=f"{member.mention} foi banido do servidor.",
                color=discord.Color.red()
            )
            if reason:
                embed.add_field(name="Motivo", value=reason, inline=False)
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message(f"❌ Erro ao banir: {str(e)}", ephemeral=True)

    # Versão com prefixo "c."
    @commands.command(name="ban", help="Bane um usuário do servidor.")
    @commands.has_permissions(ban_members=True)
    async def ban_prefix(self, ctx, member: discord.Member, *, reason=None):
        """Comando c.ban - Bane um usuário"""
        try:
            await member.ban(reason=reason)
            embed = discord.Embed(
                title="✅ Membro Banido",
                description=f"{member.mention} foi banido do servidor.",
                color=discord.Color.red()
            )
            if reason:
                embed.add_field(name="Motivo", value=reason, inline=False)
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"❌ Erro ao banir: {str(e)}")

    @ban_prefix.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ Você não tem permissão para usar este comando.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("❌ Você precisa mencionar um usuário. Exemplo: `c.ban @usuario motivo`")

    # ==========================================
    # COMANDO DE MUTE (Timeout / Castigo)
    # ==========================================
    
    # Versão Slash Command
    @app_commands.command(name="mute", description="Silencia um usuário temporariamente (Timeout).")
    @app_commands.describe(
        member="O membro a ser silenciado",
        minutes="Duração do silenciamento em minutos",
        reason="Motivo do silenciamento (opcional)"
    )
    @commands.has_permissions(moderate_members=True)
    async def mute_slash(self, interaction: discord.Interaction, member: discord.Member, minutes: int, reason: str = None):
        """Comando /mute - Silencia um usuário"""
        try:
            if minutes > 40320:  # Limite máximo do Discord (28 dias)
                await interaction.response.send_message("❌ Duração máxima é 40320 minutos (28 dias).", ephemeral=True)
                return
            
            duration = timedelta(minutes=minutes)
            await member.timeout(duration, reason=reason)
            embed = discord.Embed(
                title="✅ Membro Silenciado",
                description=f"{member.mention} foi silenciado por {minutes} minuto(s).",
                color=discord.Color.orange()
            )
            if reason:
                embed.add_field(name="Motivo", value=reason, inline=False)
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message(f"❌ Erro ao silenciar: {str(e)}", ephemeral=True)

    # Versão com prefixo "c."
    @commands.command(name="mute", help="Silencia um usuário temporariamente (Timeout).")
    @commands.has_permissions(moderate_members=True)
    async def mute_prefix(self, ctx, member: discord.Member, minutes: int, *, reason=None):
        """Comando c.mute - Silencia um usuário"""
        try:
            if minutes > 40320:  # Limite máximo do Discord (28 dias)
                await ctx.send("❌ Duração máxima é 40320 minutos (28 dias).")
                return
            
            duration = timedelta(minutes=minutes)
            await member.timeout(duration, reason=reason)
            embed = discord.Embed(
                title="✅ Membro Silenciado",
                description=f"{member.mention} foi silenciado por {minutes} minuto(s).",
                color=discord.Color.orange()
            )
            if reason:
                embed.add_field(name="Motivo", value=reason, inline=False)
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"❌ Erro ao silenciar: {str(e)}")

    @mute_prefix.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ Você não tem permissão para usar este comando.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("❌ Uso correto: `c.mute @usuario [minutos] [motivo]`")


async def setup(bot):
    await bot.add_cog(Moderacao(bot))
