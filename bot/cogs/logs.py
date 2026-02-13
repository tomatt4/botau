import discord
from discord.ext import commands
from datetime import datetime

class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    LOG_CHANNEL_ID = 1406713073720496179  # ID do canal de logs
    ALT_DAYS_LIMIT = 3

    def log_channel(self, guild):
        return guild.get_channel(self.LOG_CHANNEL_ID)

    # ===== MENSAGEM DELETADA =====
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return

        channel = self.log_channel(message.guild)
        if not channel:
            return

        embed = discord.Embed(
            title="Mensagem deletada",
            color=discord.Color.red(),
            timestamp=datetime.utcnow()
        )
        embed.add_field(name="Autor", value=f"{message.author} ({message.author.id})", inline=False)
        embed.add_field(name="Canal", value=message.channel.mention, inline=False)
        embed.add_field(name="Conteúdo", value=message.content or "Sem conteúdo", inline=False)

        await channel.send(embed=embed)

    # ===== MENSAGEM EDITADA =====
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot or before.content == after.content:
            return

        channel = self.log_channel(before.guild)
        if not channel:
            return

        embed = discord.Embed(
            title="Mensagem editada",
            color=discord.Color.orange(),
            timestamp=datetime.utcnow()
        )
        embed.add_field(name="Autor", value=f"{before.author} ({before.author.id})", inline=False)
        embed.add_field(name="Canal", value=before.channel.mention, inline=False)
        embed.add_field(name="Antes", value=before.content or "Vazio", inline=False)
        embed.add_field(name="Depois", value=after.content or "Vazio", inline=False)

        await channel.send(embed=embed)

    # ===== ALTERAÇÃO NO SERVIDOR =====
    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
        if before.name == after.name:
            return

        channel = self.log_channel(after)
        if not channel:
            return

        embed = discord.Embed(
            title="Servidor alterado",
            color=discord.Color.blue(),
            timestamp=datetime.utcnow()
        )
        embed.add_field(name="Nome antigo", value=before.name, inline=False)
        embed.add_field(name="Nome novo", value=after.name, inline=False)

        await channel.send(embed=embed)

    # ===== BAN =====
    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        channel = self.log_channel(guild)
        if not channel:
            return

        embed = discord.Embed(
            title="Usuário banido",
            color=discord.Color.dark_red(),
            timestamp=datetime.utcnow()
        )
        embed.add_field(name="Usuário", value=f"{user} ({user.id})", inline=False)

        await channel.send(embed=embed)

    # ===== UNBAN =====
    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        channel = self.log_channel(guild)
        if not channel:
            return

        embed = discord.Embed(
            title="Usuário desbanido",
            color=discord.Color.green(),
            timestamp=datetime.utcnow()
        )
        embed.add_field(name="Usuário", value=f"{user} ({user.id})", inline=False)

        await channel.send(embed=embed)

    # ===== KICK =====
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.log_channel(member.guild)
        if not channel:
            return

        async for entry in member.guild.audit_logs(limit=1):
            if entry.target.id == member.id and entry.action == discord.AuditLogAction.kick:
                embed = discord.Embed(
                    title="Usuário kickado",
                    color=discord.Color.dark_orange(),
                    timestamp=datetime.utcnow()
                )
                embed.add_field(name="Usuário", value=f"{member} ({member.id})", inline=False)
                embed.add_field(name="Por", value=entry.user, inline=False)

                await channel.send(embed=embed)
                return

    # ===== CASTIGO / TIMEOUT =====
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        channel = self.log_channel(after.guild)
        if not channel:
            return

        if before.communication_disabled_until != after.communication_disabled_until:
            if after.communication_disabled_until:
                restante = after.communication_disabled_until - datetime.utcnow()
                minutos = int(restante.total_seconds() // 60)

                embed = discord.Embed(
                    title="Usuário castigado",
                    color=discord.Color.purple(),
                    timestamp=datetime.utcnow()
                )
                embed.add_field(name="Usuário", value=f"{after} ({after.id})", inline=False)
                embed.add_field(name="Tempo restante", value=f"{minutos} minutos", inline=False)
            else:
                embed = discord.Embed(
                    title="Castigo removido",
                    color=discord.Color.green(),
                    timestamp=datetime.utcnow()
                )
                embed.add_field(name="Usuário", value=f"{after} ({after.id})", inline=False)

            await channel.send(embed=embed)

    # ===== ENTRADA + ALT CHECK =====
    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.log_channel(member.guild)
        if not channel:
            return

        idade = (datetime.utcnow() - member.created_at).days
        status = "Possível ALT" if idade < self.ALT_DAYS_LIMIT else "Conta normal"

        embed = discord.Embed(
            title="Membro entrou",
            color=discord.Color.teal(),
            timestamp=datetime.utcnow()
        )
        embed.add_field(name="Usuário", value=f"{member} ({member.id})", inline=False)
        embed.add_field(name="Conta criada em", value=member.created_at.strftime("%d/%m/%Y"), inline=False)
        embed.add_field(name="Idade da conta", value=f"{idade} dias", inline=False)
        embed.add_field(name="Status", value=status, inline=False)

        await channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Logs(bot))
