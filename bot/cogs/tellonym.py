import discord
from discord.ext import commands
from datetime import datetime, timedelta

from utils.gerar_imagem import gerar_imagem_tellonym
from db import add_tellonym, get_conn

# 🔧 CONFIGURAÇÕES
CANAL_TELLONYM_ID = 1474178044586627317
COOLDOWN_MINUTOS = 60


# ───────────── MODAL ─────────────
class TellonymModal(discord.ui.Modal, title="Enviar mensagem anônima"):
    mensagem = discord.ui.TextInput(
        label="Sua mensagem",
        style=discord.TextStyle.paragraph,
        max_length=500,
        placeholder="Escreva aqui anonimamente..."
    )

    async def on_submit(self, interaction: discord.Interaction):
        membro = interaction.user

        # 👑 Admin sem cooldown
        if not membro.guild_permissions.administrator:
            conn = get_conn()
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT created_at FROM tellonym
                    WHERE user_id = %s
                    ORDER BY created_at DESC
                    LIMIT 1
                    """,
                    (membro.id,)
                )
                ultima = cur.fetchone()
            conn.close()

            if ultima:
                ultima_data = ultima[0]
                if datetime.utcnow() - ultima_data < timedelta(minutes=COOLDOWN_MINUTOS):
                    await interaction.response.send_message(
                        "⏳ Você só pode enviar **1 tellonym por hora**.",
                        ephemeral=True
                    )
                    return

        # 💾 Salva no banco
        tellonym_id = add_tellonym(membro.id, self.mensagem.value)

        # 🖼️ Gera imagem
        caminho_img = gerar_imagem_tellonym(
            numero=tellonym_id,
            mensagem=self.mensagem.value,
        )

        canal = interaction.guild.get_channel(CANAL_TELLONYM_ID)

        embed = discord.Embed(
            title="📩 Novo Tellonym Anônimo",
            color=discord.Color.purple(),
            timestamp=datetime.utcnow()
        )

        embed.set_image(url="attachment://tellonym.png")

        file = discord.File(caminho_img, filename="tellonym.png")
        await canal.send(embed=embed, file=file)

        await interaction.response.send_message(
            "✅ Sua mensagem foi enviada anonimamente!",
            ephemeral=True
        )


# ───────────── VIEW COM BOTÃO ─────────────
class TellonymView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="📩 Enviar mensagem anônima",
        style=discord.ButtonStyle.primary,
        custom_id="tellonym_button"
    )
    async def enviar(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(TellonymModal())


# ───────────── COG ─────────────
class Tellonym(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="painel_tellonym")
    @commands.has_permissions(administrator=True)
    async def painel_tellonym(self, ctx):
        """Envia o painel do Tellonym"""

        embed = discord.Embed(
            title="💬 Tellonym do Servidor",
            description=(
                "Envie mensagens **totalmente anônimas** 📭\n\n"
                "• 1 mensagem por hora\n"
                "• Administradores não possuem limite\n"
                "• Respeite as regras do servidor"
            ),
            color=discord.Color.blurple()
        )

        await ctx.send(embed=embed, view=TellonymView())


async def setup(bot):
    await bot.add_cog(Tellonym(bot))
