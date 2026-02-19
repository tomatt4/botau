import discord
from discord.ext import commands

INVITE_LINK = "https://discord.gg/h3nmQEGpq6"
CARGO_ID = 123456789012345678  # Coloque o ID do cargo

class PrimeiraDamaView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label="Verificar", style=discord.ButtonStyle.success, emoji="🔍")
    async def verificar(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.guild.get_member(interaction.user.id)
        if not member:
            await interaction.response.send_message(
                "Não consegui te encontrar no servidor.",
                ephemeral=True
            )
            return

        cargo = interaction.guild.get_role(CARGO_ID)
        if not cargo:
            await interaction.response.send_message(
                "Cargo não encontrado no servidor.",
                ephemeral=True
            )
            return

        await interaction.response.defer(ephemeral=True)

        try:
            user = interaction.user  # pega o User
            bio = user.bio or ""     # bio pública

            if INVITE_LINK.lower() in bio.lower():
                await member.add_roles(cargo)
                await member.send(
                    "✅ **Verificação aprovada!** Cargo **Primeira Dama** concedido 🎉"
                )
            else:
                await member.send(
                    "❌ Link do servidor não encontrado na sua bio.\n"
                    f"Por favor, adicione `{INVITE_LINK}` na sua bio e tente novamente."
                )

        except discord.Forbidden:
            await interaction.followup.send(
                "Não consigo enviar DM pra você. Ative suas DMs e tente novamente.",
                ephemeral=True
            )
        except Exception as e:
            await interaction.followup.send(
                f"Ocorreu um erro ao verificar sua bio: {e}",
                ephemeral=True
            )


class PrimeiraDama(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def primeiradama(self, ctx):
        embed = discord.Embed(
            title="Cargo Primeira Dama",
            description=(
                "O cargo **Primeira Dama** é um cargo especial para quem ajuda "
                "a divulgar o servidor\n\n"
                "Ao clicar em **Verificar**, o bot vai checar sua bio "
                "automaticamente para confirmar se o link do servidor está visível."
            ),
            color=discord.Color.pink()
        )

        embed.add_field(
            name="Benefícios",
            value=(
                "3x EXP\n"
                "Pode conceder o cargo para até 2 pessoas\n"
                "GIFs, áudios e anexos liberados\n"
                "Prioridade nas calls"
            ),
            inline=False
        )

        embed.add_field(
            name="Como obter",
            value=(
                f"• Coloque o link `{INVITE_LINK}` na sua bio\n"
                "• Clique em **Verificar**"
            ),
            inline=False
        )

        await ctx.send(embed=embed, view=PrimeiraDamaView(self.bot))


async def setup(bot):
    await bot.add_cog(PrimeiraDama(bot))
