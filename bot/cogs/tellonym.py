import discord
from discord.ext import commands
from datetime import datetime, timedelta

from utils.gerar_imagem import gerar_imagem_tellonym
from db import add_tellonym, get_conn

# :wrench: CONFIGURAÇÕES
CANAL_TELLONYM_ID = 1474254658662039713  # canal público do tellonym
STAFF_LOG_ID = 1406713073720496179       # canal de logs da staff
COOLDOWN_MINUTOS = 60


# ───────────── MODAL ─────────────
class TellonymModal(discord.ui.Modal, title="Enviar mensagem anônima"):
    mensagem = discord.ui.TextInput(
        label="Sua mensagem",
        style=discord.TextStyle.paragraph,
        max_length=104,
        placeholder="Escreva aqui anonimamente."
    )

    async def on_submit(self, interaction: discord.Interaction):
        membro = interaction.user

        # :crown: Administradores não têm cooldown
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
                        "Você só pode enviar **1 tellonym por hora**.",
                        ephemeral=True
                    )
                    return

        # :floppy_disk: Salva no banco de dados e pega o ID
        tellonym_id = add_tellonym(membro.id, self.mensagem.value)

        # :frame_photo: Gera a imagem do tellonym
        caminho_img = gerar_imagem_tellonym(
            numero=tellonym_id,
            mensagem=self.mensagem.value,
        )

        # :small_blue_diamond: Envia no canal público anonimamente
        canal_publico = interaction.guild.get_channel(CANAL_TELLONYM_ID)
        file = discord.File(caminho_img, filename="tellonym.png")
        embed_publico = discord.Embed(
            title="Novo Tellonym Anônimo",
            description="Conteúdo inaproriado abaixo? **Denuncie imediatamente.**",
            color=0xFFFFFF,
            timestamp=datetime.utcnow()
        )
        embed_publico.set_image(url="attachment://tellonym.png")
        await canal_publico.send(embed=embed_publico, file=file)

        # :small_blue_diamond: Envia log para staff mencionando quem enviou
        canal_log = interaction.guild.get_channel(STAFF_LOG_ID)
        embed_log = discord.Embed(
            title="Log de Tellonym",
            description=f"O membro {membro.mention} enviou um tellonym: `{self.mensagem.value}`",
            color=discord.Color.orange(),
            timestamp=datetime.utcnow()
        )
        await canal_log.send(embed=embed_log)

        # Confirmação para quem enviou
        await interaction.response.send_message(
            "Sua mensagem foi enviada anonimamente!",
            ephemeral=True
        )


# ───────────── VIEW COM BOTÃO ─────────────
class TellonymView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Enviar mensagem anônima",
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
            title="Tellonym do Servidor",
            description=(
                "**O que é um Tellonym?**\n\n"
                "Um Tellonym é uma mensagem anônima enviada por alguém do servidor. "
                f"As mensagens aparecem no canal <#{CANAL_TELLONYM_ID}> "
                "como uma imagem estilizada, sem mostrar quem enviou. "
                "Você pode enviar mensagens anonimamente clicando no botão abaixo."
            ),
            color=0xFFFFFF
        )

        await ctx.send(embed=embed, view=TellonymView())


# ───────────── SETUP ─────────────
async def setup(bot):
    await bot.add_cog(Tellonym(bot))
