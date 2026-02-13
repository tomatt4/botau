import discord
from discord.ext import commands
from datetime import timedelta
from db import get_conn


# =========================
# VIEW DO TICKET (PERSISTENTE)
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

        # 💾 Salvar no banco
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

        exclusive_role_mention = "<@&1447395230646140999>"

        await interaction.response.send_message(
            f"Ticket criado brother: {channel.mention}",
            ephemeral=True,
        )

        await channel.send(
            f"{interaction.user.mention} {exclusive_role_mention}\n\n"
            f"***Boas vindas ao seu Ticket!***\n"
            f"Este canal é o seu ticket, e é aqui que você receberá o seu atendimento.\n"
            f"Apenas **administradores** podem visualizar esse canal.\n\n"
            f"***Tipo do ticket:*** **{ticket_type}**\n"
            f"Um administrador irá te atender em breve."
        )


# =========================
# COG ADMIN
# =========================
class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="painel",
        description="Criar painel de tickets",
    )
    @commands.has_permissions(administrator=True)
    async def painel(self, ctx: commands.Context):
        embed = discord.Embed(
            title="Sistema de Suporte SPHB",
            description=(
                "Boas vindas ao Sistema de Suporte Profissional da Spider Hub via **tickets**!\n\n"
                "Para saber mais sobre a função dos tickets, selecione abaixo no **Select Menu** "
                "o tipo de ajuda que você quer."
            ),
            color=0xFFFFFF,
        )
        embed.set_footer(text="Sistema de Suporte SPHB feito por Salvador")

        view = TicketView()

        if ctx.interaction:
            await ctx.interaction.response.send_message(embed=embed, view=view)
        else:
            await ctx.send(embed=embed, view=view)

    @commands.hybrid_command(
        name="fechar",
        description="Fechar o ticket atual",
    )
    @commands.has_permissions(administrator=True)
    async def fechar(self, ctx: commands.Context):
        conn = get_conn()
        cur = conn.cursor()

        cur.execute(
            "SELECT id FROM tickets WHERE channel_id = %s",
            (str(ctx.channel.id),),
        )
        result = cur.fetchone()

        if not result:
            msg = "Este canal não é um ticket registrado."
            if ctx.interaction:
                await ctx.interaction.response.send_message(msg, ephemeral=True)
            else:
                await ctx.send(msg)

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

        aviso = "Ticket será fechado em **10 segundos** ⏳"

        if ctx.interaction:
            await ctx.interaction.response.send_message(aviso)
        else:
            await ctx.send(aviso)

        await discord.utils.sleep_until(
            discord.utils.utcnow() + timedelta(seconds=10)
        )
        await ctx.channel.delete(reason=f"Ticket fechado por {ctx.author}")


async def setup(bot):
    await bot.add_cog(Admin(bot))
