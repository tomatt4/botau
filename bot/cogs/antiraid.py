# cogs/antiraid.py
import discord
from discord.ext import commands
from discord import app_commands

class AntiRaid(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.backup_roles = {}
        self.backup_channel_perms = {}
        self.active = False  # Marca se o antiraid tá ativo

    # ====================
    # Comando AntiRaid
    # ====================
    @app_commands.command(name="antiraid", description="Ativa proteção anti-raid")
    @app_commands.checks.has_permissions(administrator=True)
    async def antiraid(self, interaction: discord.Interaction):
        guild = interaction.guild
        self.active = True

        # 1️⃣ Banir bots não verificados
        for member in guild.members:
            if member.bot and member != self.bot.user:
                try:
                    await member.ban(reason="Anti-Raid")
                except:
                    # Remove permissões caso não consiga banir
                    try:
                        await member.edit(roles=[])
                    except:
                        pass

        # 2️⃣ Bloquear envio de mensagem para @everyone
        everyone_role = guild.default_role
        self.backup_roles["everyone"] = everyone_role.permissions
        perms = everyone_role.permissions
        perms.update(send_messages=False)
        await everyone_role.edit(permissions=perms)

        # Backup canais
        self.backup_channel_perms.clear()
        for channel in guild.channels:
            self.backup_channel_perms[channel.id] = channel.permissions_synced

        await interaction.response.send_message("Anti-Raid ativado!", ephemeral=True)

    # ====================
    # Comando Restaurar
    # ====================
    @app_commands.command(name="restaurar", description="Desativa anti-raid e restaura servidor")
    @app_commands.checks.has_permissions(administrator=True)
    async def restaurar(self, interaction: discord.Interaction):
        guild = interaction.guild
        self.active = False

        # Restaurar permissões do everyone
        if "everyone" in self.backup_roles:
            await guild.default_role.edit(permissions=self.backup_roles["everyone"])

        # Restaurar canais
        for channel_id, synced in self.backup_channel_perms.items():
            channel = guild.get_channel(channel_id)
            if channel:
                await channel.edit(sync_permissions=True)

        await interaction.response.send_message("Servidor restaurado!", ephemeral=True)

    # ====================
    # Eventos AntiRaid
    # ====================
    @commands.Cog.listener()
    async def on_message(self, message):
        if not self.active or message.author == self.bot.user:
            return

        # 3️⃣ Mensagens rápidas
        if (discord.utils.utcnow() - message.created_at).total_seconds() < 3:
            await message.delete()
            return

        # 4️⃣ Mentions @everyone
        if "@everyone" in message.content:
            await message.delete()
            return

        # 5️⃣ Convites
        if "discord.gg/" in message.content:
            await message.delete()
            return

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        if self.active:
            await channel.delete(reason="Anti-Raid: Canal criado")

async def setup(bot):
    await bot.add_cog(AntiRaid(bot))
