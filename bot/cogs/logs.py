import discord
from discord.ext import commands
from datetime import datetime, timedelta

class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ========= CONFIG =========
    LOG_CHANNEL_ID = 1454971586758180907  # ID do canal de logs
    ALT_DAYS_LIMIT = 3  # conta com menos de X dias = possível alt

    def get_log_channel(self, guild):
        return guild.get_channel(self.LOG_CHANNEL_ID)

    # ========= MENSAGEM DELETADA =========
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return

        channel = self.get_log_channel(message.guild)
        if not channel:
            return

        await channel.send(
            f"Mensagem deletada\n"
            f"Autor: {message.author} ({message.author.id})\n"
            f"Canal: {message.channel.mention}\n"
            f"Conteúdo: {message.content}"
        )

    # ========= MENSAGEM EDITADA =========
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot or before.content == after.content:
            return

        channel = self.get_log_channel(before.guild)
        if not channel:
            return

        await channel.send(
            f"Mensagem editada\n"
            f"Autor: {before.author} ({before.author.id})\n"
            f"Canal: {before.channel.mention}\n"
            f"Antes: {before.content}\n"
            f"Depois: {after.content}"
        )

    # ========= ALTERAÇÕES NO SERVIDOR =========
    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
        channel = self.get_log_channel(after)
        if not channel:
            return

        if before.name != after.name:
            await channel.send(
                f"Nome do servidor alterado\n"
                f"Antes: {before.name}\n"
                f"Depois: {after.name}"
            )

    # ========= BAN =========
    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        channel = self.get_log_channel(guild)
        if not channel:
            return

        await channel.send(
            f"Usuário banido\n"
            f"Usuário: {user} ({user.id})"
        )

    # ========= UNBAN =========
    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        channel = self.get_log_channel(guild)
        if not channel:
            return

        await channel.send(
            f"Usuário desbanido\n"
            f"Usuário: {user} ({user.id})"
        )

    # ========= KICK =========
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        # Não dá pra diferenciar saída normal de kick 100% sem audit log
        channel = self.get_log_channel(member.guild)
        if not channel:
            return

        async for entry in member.guild.audit_logs(limit=1):
            if entry.target.id == member.id and entry.action == discord.AuditLogAction.kick:
                await channel.send(
                    f"Usuário kickado\n"
                    f"Usuário: {member} ({member.id})\n"
                    f"Por: {entry.user}"
                )
                return

    # ========= CASTIGO / TIMEOUT =========
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        channel = self.get_log_channel(after.guild)
        if not channel:
            return

        # Timeout aplicado
        if before.communication_disabled_until != after.communication_disabled_until:
            if after.communication_disabled_until:
                restante = after.communication_disabled_until - datetime.utcnow()
                minutos = int(restante.total_seconds() // 60)

                await channel.send(
                    f"Usuário castigado (timeout)\n"
                    f"Usuário: {after} ({after.id})\n"
                    f"Tempo restante: {minutos} minutos"
                )
            else:
                await channel.send(
                    f"Castigo removido\n"
                    f"Usuário: {after} ({after.id})"
                )

    # ========= MEMBRO ENTROU (ALT CHECK) =========
    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.get_log_channel(member.guild)
        if not channel:
            return

        conta_idade = datetime.utcnow() - member.created_at
        dias = conta_idade.days

        alt_status = "POSSÍVEL ALT." if dias < self.ALT_DAYS_LIMIT else "Conta normal."

        await channel.send(
            f"Membro entrou no servidor\n"
            f"Usuário: {member} ({member.id})\n"
            f"Criou a conta em: {member.created_at.strftime('%d/%m/%Y')}\n"
            f"Idade da conta: {dias} dias\n"
            f"Status: **{alt_status}**"
        )

async def setup(bot):
    await bot.add_cog(Logs(bot))
