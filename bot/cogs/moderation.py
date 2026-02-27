import discord
from discord import app_commands
from discord.ext import commands
from datetime import timedelta
import asyncio
from db import get_conn

# =========================
# 🎫 VIEW DO TICKET (PERSISTENTE)
# =========================
class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.select(
        placeholder="Selecione uma opção de atendimento.",
        custom_id="ticket_select",
        options=[
            discord.SelectOption(
                label="Denunciar",
                description="Reportar algo para a staff",
                value="denúncia",
            ),
            discord.SelectOption(
                label="Sugestão",
                description="Enviar uma ideia ou sugestão",
                value="sugestão",
            ),
            discord.SelectOption(
                label="Suporte",
                description="Precisa de ajuda?",
                value="suporte",
            ),
        ],
    )
    async def select_callback(
        self,
        interaction: discord.Interaction,
        select: discord.ui.Select,
    ):
        await self.create_ticket(interaction, select.values[0])

    async def create_ticket(self, interaction: discord.Interaction, ticket_type: str):
        if not interaction.guild:
            await interaction.response.send_message(
                "Este comando só pode ser usado em um servidor.",
                ephemeral=True,
            )
            return

        guild = interaction.guild

        # 📁 Categoria
        category = discord.utils.get(guild.categories, name="𝐒𝐮𝐩𝐨𝐫𝐭𝐞")
        if category is None:
            category = await guild.create_category("𝐒𝐮𝐩𝐨𝐫𝐭𝐞")

        # 🔐 Permissões
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        }

        for role in guild.roles:
            if role.permissions.administrator:
                overwrites[role] = discord.PermissionOverwrite(
                    read_messages=True, send_messages=True
                )

        channel_name = f"{ticket_type.lower()}-{interaction.user.name}"

        channel = await guild.create_text_channel(
            name=channel_name,
            category=category,
            overwrites=overwrites,
        )

        # 💾 Banco
        try:
            conn = get_conn()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO tickets (user_id, channel_id, type) VALUES (%s, %s, %s)",
                (str(interaction.user.id), str(channel.id), ticket_type),
            )
            conn.commit()
        finally:
            cur.close()
            conn.close()

        await interaction.response.send_message(
            f"Ticket criado: {channel.mention}",
            ephemeral=True,
        )

        await channel.send(
            f"{interaction.user.mention}\n\n"
            f"***Boas vindas ao seu Ticket!***\n"
            f"Tipo: **{ticket_type}**\n"
            f"Um administrador irá te atender em breve."
        )

# =========================
# 🔨 COG MODERATION
# =========================
class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 🔒 Checagem global
    async def cog_check(self, ctx: commands.Context):
        return ctx.author.guild_permissions.administrator

    # =====================
    # 🎫 PAINEL DE TICKETS
    # =====================
    @commands.hybrid_command(name="painel", description="Criar painel de tickets")
    async def painel(self, ctx: commands.Context):
        embed = discord.Embed(
            title="Sistema de Suporte",
            description=(
                "Selecione abaixo o tipo de atendimento desejado."
            ),
            color=0xFFFFFF,
        )

        view = TicketView()

        if ctx.interaction:
            await ctx.interaction.response.send_message(embed=embed, view=view)
        else:
            await ctx.send(embed=embed, view=view)

    # =====================
    # 👤 ASSUMIR TICKET
    # =====================
    @commands.hybrid_command(name="assumir", description="Assumir o ticket atual")
    async def assumir(self, ctx: commands.Context):
        conn = get_conn()
        cur = conn.cursor()

        cur.execute(
            "SELECT id FROM tickets WHERE channel_id = %s",
            (str(ctx.channel.id),),
        )
        result = cur.fetchone()

        cur.close()
        conn.close()

        if not result:
            msg = "Este canal não é um ticket."
            if ctx.interaction:
                await ctx.interaction.response.send_message(msg, ephemeral=True)
            else:
                await ctx.send(msg)
            return

        await ctx.send("Ticket assumido com sucesso.")

    # =====================
    # ❌ FECHAR TICKET
    # =====================
    @commands.hybrid_command(name="fechar", description="Fechar o ticket atual")
    async def fechar(self, ctx: commands.Context):
        conn = get_conn()
        cur = conn.cursor()

        cur.execute(
            "SELECT id FROM tickets WHERE channel_id = %s",
            (str(ctx.channel.id),),
        )
        result = cur.fetchone()

        if not result:
            await ctx.send("Este canal não é um ticket.")
            cur.close()
            conn.close()
            return

        cur.execute(
            "DELETE FROM tickets WHERE channel_id = %s",
            (str(ctx.channel.id),),
        )
        conn.commit()
        cur.close()
        conn.close()

        await ctx.send("Ticket será fechado em **10 segundos** ⏳")
        await asyncio.sleep(10)
        await ctx.channel.delete()

    # =====================
    # 🔨 BAN
    # =====================
    @commands.hybrid_command(name="ban", description="Banir um usuário")
    async def ban(
        self,
        ctx: commands.Context,
        user: discord.Member,
        *,
        reason: str = "Nenhum motivo fornecido.",
    ):
        await user.ban(reason=reason)
        await ctx.send(f"**{user}** foi banido. Motivo: {reason}")

    # =====================
    # 👢 KICK
    # =====================
    @commands.hybrid_command(name="kick", description="Expulsar um usuário")
    async def kick(
        self,
        ctx: commands.Context,
        user: discord.Member,
        *,
        reason: str = "Nenhum motivo fornecido.",
    ):
        await user.kick(reason=reason)
        await ctx.send(f"**{user}** foi expulso. Motivo: {reason}")

    # =====================
    # 🔇 MUTE
    # =====================
    @commands.hybrid_command(name="mute", description="Silenciar um usuário")
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
        await ctx.send(f"{user.mention} silenciado por {time} minutos.")

    # =====================
    # ⚠️ WARN
    # =====================
    @commands.hybrid_command(name="warn", description="Avisar um usuário")
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

        await ctx.send(f"{user.mention} recebeu um warn. Motivo: {reason}")

# =========================
# SETUP
# =========================
async def setup(bot):
    await bot.add_cog(Moderation(bot))
