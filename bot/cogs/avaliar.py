# arquivo: avaliar.py
import discord
from discord.ext import commands
import asyncio

STAFF_ROLE_ID = 1447395230646140999  # ID do cargo de staff


class StaffEvaluation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="avaliar_staff")
    async def avaliar_staff(self, ctx):
        """Envia a embed com botão para avaliar staff"""

        embed = discord.Embed(
            title="Avaliação de Staff",
            description="Clique no botão abaixo para avaliar um membro da staff!",
            color=0xFFFFFF
        )

        view = AvaliarView(self.bot)
        await ctx.send(embed=embed, view=view)


class AvaliarView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label="Avaliar Staff", style=discord.ButtonStyle.green)
    async def avaliar_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild

        staff_membros = [
            m for m in guild.members
            if any(r.id == STAFF_ROLE_ID for r in m.roles)
        ]

        if not staff_membros:
            await interaction.response.send_message(
                "Não encontrei nenhum membro com o cargo de staff.",
                ephemeral=True
            )
            return

        view = StaffSelect(self.bot, guild, staff_membros)
        await interaction.response.send_message(
            "Escolha o staff abaixo:",
            view=view,
            ephemeral=True
        )


class StaffSelect(discord.ui.View):
    def __init__(self, bot, guild, staff_membros):
        super().__init__(timeout=180)
        self.bot = bot
        self.guild = guild

        options = [
            discord.SelectOption(
                label=m.display_name,
                value=str(m.id)
            )
            for m in staff_membros
        ]

        select = discord.ui.Select(
            placeholder="Escolha o staff que deseja avaliar",
            min_values=1,
            max_values=1,
            options=options
        )

        select.callback = self.select_callback
        self.add_item(select)

    async def select_callback(self, interaction: discord.Interaction):
        staff_id = int(interaction.data["values"][0])
        staff_user = self.guild.get_member(staff_id)

        if staff_user is None:
            await interaction.response.send_message(
                "Não consegui encontrar esse usuário.",
                ephemeral=True
            )
            return

        try:
            await interaction.user.send(
                f"Você escolheu avaliar **{staff_user.display_name}**.\n"
                "Envie sua avaliação aqui. Você tem 5 minutos."
            )

            await interaction.response.send_message(
                "Te enviei uma DM para enviar sua avaliação!",
                ephemeral=True
            )

        except discord.Forbidden:
            await interaction.response.send_message(
                "Não consegui te enviar DM. Verifique suas configurações.",
                ephemeral=True
            )
            return

        def check(m):
            return (
                m.author == interaction.user
                and isinstance(m.channel, discord.DMChannel)
            )

        try:
            msg = await self.bot.wait_for(
                "message",
                check=check,
                timeout=300
            )
        except asyncio.TimeoutError:
            await interaction.user.send(
                "Tempo esgotado. Tente novamente clicando no botão."
            )
            return

        try:
            await staff_user.send(
                f"**Nova avaliação recebida!**\n\n"
                f"{interaction.user.mention} deu a seguinte avaliação para você: **{msg.content}**"
            )
            await interaction.user.send(
                "Sua avaliação foi enviada com sucesso."
            )

        except discord.Forbidden:
            await interaction.user.send(
                "Não consegui enviar a avaliação ao staff (DMs fechadas)."
            )


async def setup(bot):
    await bot.add_cog(StaffEvaluation(bot))
