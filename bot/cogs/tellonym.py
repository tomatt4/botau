import discord
from discord.ext import commands
from datetime import timedelta, datetime

from db import save_tellonym, get_last_tellonym_time


# =========================
# MODAL (FORMULÁRIO)
# =========================
class TellonymModal(discord.ui.Modal, title="Enviar Tellonym"):
    mensagem = discord.ui.TextInput(
        label="Mensagem anônima",
        style=discord.TextStyle.paragraph,
        placeholder="Escreva o que quiser 👀",
        max_length=500
    )

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    async def on_submit(self, interaction: discord.Interaction):
        member = interaction.user

        # ADMIN IGNORA COOLDOWN
        if not member.guild_permissions.administrator:
            last_time = get_last_tellonym_time(member.id)

            if last_time:
                if datetime.utcnow() - last_time < timedelta(hours=1):
                    restante = timedelta(hours=1) - (datetime.utcnow() - last_time)
                    minutos = int(restante.total_seconds() // 60)

                    await interaction.response.send_message(
                        f"⏳ Calma aí! Espere **{minutos} min** pra mandar outro tellonym.",
                        ephemeral=True
                    )
                    return

        save_tellonym(member.id, self.mensagem.value)

        embed = discord.Embed(
            title="📩 Tellonym Anônimo",
            description=self.mensagem.value,
            color=discord.Color.purple(),
            timestamp=datetime.utcnow()
        )
        embed.set_footer(text="Mensagem enviada anonimamente")

        await interaction.channel.send(embed=embed)

        await interaction.response.send_message(
            "✅ Tellonym enviado com sucesso!",
            ephemeral=True
        )


# =========================
# VIEW COM BOTÃO
# =========================
class TellonymView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.Button(
        label="📨 Enviar Tellonym",
        style=discord.ButtonStyle.primary
    )
    async def send_tellonym(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        await interaction.response.send_modal(TellonymModal(self.bot))


# =========================
# COG
# =========================
class Tellonym(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="tellonym")
    @commands.has_permissions(administrator=True)
    async def tellonym_panel(self, ctx):
        embed = discord.Embed(
            title="💬 Tellonym do Servidor",
            description=(
                "Envie mensagens **anonimamente** para o servidor.\n\n"
                "• 1 tellonym por hora\n"
                "• Administradores não têm cooldown\n"
                "• Totalmente anônimo 👻"
            ),
            color=discord.Color.purple()
        )

        await ctx.send(embed=embed, view=TellonymView(self.bot))


async def setup(bot):
    await bot.add_cog(Tellonym(bot))
