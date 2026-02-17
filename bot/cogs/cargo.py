import discord
from discord import app_commands
from discord.ext import commands

VIP_ID = 1447756713146056745
MAIORAL_ID = 1458661267572133939

ROLE_ABAIXO = 1451412244029116436
ROLE_ACIMA = 1473093782386905304

def tem_permissao(member: discord.Member):
    return any(role.id in (VIP_ID, MAIORAL_ID) for role in member.roles)

# ─────────────────────────────
# MODAL (FORMULÁRIO)
# ─────────────────────────────
class CargoModal(discord.ui.Modal, title="Criar Cargo Personalizado"):

    nome = discord.ui.TextInput(
        label="Nome do cargo",
        placeholder="Ex: Elite, Campeão, Lendário",
        max_length=50
    )

    def __init__(self, interaction: discord.Interaction):
        super().__init__()
        self.interaction = interaction

    async def on_submit(self, interaction: discord.Interaction):

        guild = interaction.guild
        nome_cargo = f"/{self.nome.value.strip()}"

        # cria o cargo
        cargo = await guild.create_role(
            name=nome_cargo,
            reason=f"Cargo VIP criado por {interaction.user}"
        )

        # posiciona o cargo
        role_acima = guild.get_role(ROLE_ACIMA)
        await cargo.edit(position=role_acima.position - 1)

        # entrega o cargo
        await interaction.user.add_roles(cargo)

        await interaction.response.send_message(
            f"Cargo **{cargo.name}** criado com sucesso!\n"
            f"Um admin pode definir a cor depois.",
            ephemeral=True
        )

# ─────────────────────────────
# COG
# ─────────────────────────────
class CargoPersonalizado(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="cargo",
        description="Criar cargo personalizado (VIP / Maioral)"
    )
    async def cargo(self, interaction: discord.Interaction):

        if not tem_permissao(interaction.user):
            return await interaction.response.send_message(
                "❌ Você não tem permissão pra usar esse comando.",
                ephemeral=True
            )

        await interaction.response.send_modal(
            CargoModal(interaction)
        )

async def setup(bot):
    await bot.add_cog(CargoPersonalizado(bot))
