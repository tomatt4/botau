import discord
from discord.ext import commands
from discord import app_commands

# Cargos FIXOS para recrutamento
CARGOS_RECRUTAMENTO = [
    1447395230646140999,
    1446681471338283029,
    1436907465923891210
]

class GestaoStaff(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # =========================
    # RECRUTAR
    # =========================
    @app_commands.command(
        name="recrutar",
        description="Recruta um usuário e adiciona os cargos da staff"
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def recrutar(self, interaction: discord.Interaction, membro: discord.Member):
        for cargo_id in CARGOS_RECRUTAMENTO:
            cargo = interaction.guild.get_role(cargo_id)
            if cargo and cargo not in membro.roles:
                await membro.add_roles(cargo)

        await interaction.response.send_message(
            f"{membro.mention} foi recrutado para a staff.",
            
        )

    # =========================
    # SUBIR CARGO
    # =========================
    @app_commands.command(
        name="subir",
        description="Sobe o usuário para o próximo cargo acima"
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def subir(self, interaction: discord.Interaction, membro: discord.Member):
        cargos = sorted(
            [r for r in membro.roles if r != interaction.guild.default_role],
            key=lambda r: r.position
        )

        if not cargos:
            await interaction.response.send_message(
                "O usuário não possui cargos para subir.",
                ephemeral=True
            )
            return

        cargo_atual = cargos[-1]

        cargos_acima = [
            r for r in interaction.guild.roles
            if r.position > cargo_atual.position
            and not r.managed
        ]

        if not cargos_acima:
            await interaction.response.send_message(
                "Esse usuário já está no cargo mais alto.",
                ephemeral=True
            )
            return

        proximo_cargo = min(cargos_acima, key=lambda r: r.position)

        await membro.remove_roles(cargo_atual)
        await membro.add_roles(proximo_cargo)

        await interaction.response.send_message(
            f"{membro.mention} foi promovido de **{cargo_atual.name}** para **{proximo_cargo.name}**.",
            
        )

    # =========================
    # DESCER CARGO
    # =========================
    @app_commands.command(
        name="descer",
        description="Desce o usuário para o cargo imediatamente abaixo"
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def descer(self, interaction: discord.Interaction, membro: discord.Member):
        cargos = sorted(
            [r for r in membro.roles if r != interaction.guild.default_role],
            key=lambda r: r.position
        )

        if not cargos:
            await interaction.response.send_message(
                "O usuário não possui cargos para descer.",
                ephemeral=True
            )
            return

        cargo_atual = cargos[-1]

        cargos_abaixo = [
            r for r in interaction.guild.roles
            if r.position < cargo_atual.position
            and r != interaction.guild.default_role
        ]

        if not cargos_abaixo:
            await interaction.response.send_message(
                "Esse usuário já está no cargo mais baixo.",
                ephemeral=True
            )
            return

        cargo_inferior = max(cargos_abaixo, key=lambda r: r.position)

        await membro.remove_roles(cargo_atual)
        await membro.add_roles(cargo_inferior)

        await interaction.response.send_message(
            f"{membro.mention} foi rebaixado de **{cargo_atual.name}** para **{cargo_inferior.name}**.",


            )

async def setup(bot: commands.Bot):
    await bot.add_cog(GestaoStaff(bot))
