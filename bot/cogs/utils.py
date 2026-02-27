import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime, timedelta
import random
import asyncio

from db import (
    get_conn,
    add_tellonym,
    get_stats
)
from utils.gerar_imagem import gerar_imagem_tellonym

# =========================
# CONFIGS
# =========================
CANAL_TELLONYM_ID = 1474254658662039713
STAFF_LOG_ID = 1474263449818366114
COOLDOWN_MINUTOS = 60
STAFF_ROLE_ID = 1447395230646140999
EXCLUSIVE_ROLE_ID = 1447395230646140999

# =========================
# VIEW PRIMEIRA DAMA
# =========================
class PrimeiraDamaView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label="Resgatar", style=discord.ButtonStyle.success)
    async def resgatar(self, interaction: discord.Interaction, _):
        guild = interaction.guild
        user = interaction.user

        category = discord.utils.get(guild.categories, name="𝐈𝐧𝐟𝐨𝐫𝐦𝐚çõ𝐞𝐬")
        if not category:
            category = await guild.create_category("𝐈𝐧𝐟𝐨𝐫𝐦𝐚çõ𝐞𝐬")

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True),
        }

        for role in guild.roles:
            if role.permissions.administrator:
                overwrites[role] = discord.PermissionOverwrite(read_messages=True)

        channel = await guild.create_text_channel(
            f"primeira-dama-{user.name}",
            category=category,
            overwrites=overwrites
        )

        await interaction.response.send_message(
            f"Ticket criado: {channel.mention}",
            ephemeral=True
        )

# =========================
# TELLONYM
# =========================
class TellonymModal(discord.ui.Modal, title="Enviar mensagem anônima"):
    mensagem = discord.ui.TextInput(
        label="Mensagem",
        style=discord.TextStyle.paragraph,
        max_length=104
    )

    async def on_submit(self, interaction: discord.Interaction):
        membro = interaction.user

        if not membro.guild_permissions.administrator:
            conn = get_conn()
            cur = conn.cursor()
            cur.execute(
                "SELECT created_at FROM tellonym WHERE user_id=%s ORDER BY created_at DESC LIMIT 1",
                (membro.id,)
            )
            ultima = cur.fetchone()
            cur.close()
            conn.close()

            if ultima and datetime.utcnow() - ultima[0] < timedelta(minutes=COOLDOWN_MINUTOS):
                await interaction.response.send_message(
                    "Você só pode enviar **1 tellonym por hora**.",
                    ephemeral=True
                )
                return

        tellonym_id = add_tellonym(membro.id, self.mensagem.value)
        img = gerar_imagem_tellonym(tellonym_id, self.mensagem.value)

        canal = interaction.guild.get_channel(CANAL_TELLONYM_ID)
        file = discord.File(img, filename="tellonym.png")

        embed = discord.Embed(
            title="Novo Tellonym Anônimo",
            color=0xFFFFFF,
            timestamp=datetime.utcnow()
        )
        embed.set_image(url="attachment://tellonym.png")

        await canal.send(embed=embed, file=file)
        await interaction.response.send_message(
            "Mensagem enviada anonimamente!",
            ephemeral=True
        )

class TellonymView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Enviar mensagem anônima", style=discord.ButtonStyle.primary)
    async def enviar(self, interaction: discord.Interaction, _):
        await interaction.response.send_modal(TellonymModal())

# =========================
# COG UTILS
# =========================
class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.afk_users = {}

    # -------- EMBEDS VIP --------
    @commands.command(name="cinco_embeds")
    async def cinco_embeds(self, ctx):
        embeds = [
            discord.Embed(description="# VIP 1\nPreço: 45.6K", color=0xFFFFFF),
            discord.Embed(description="# VIP 2\nPreço: 50K", color=0xFFFFFF),
            discord.Embed(description="# VIP 3\nPreço: 58.5K", color=0xFFFFFF),
            discord.Embed(description="# VIP 4\nPreço: 65.1K", color=0xFFFFFF),
            discord.Embed(description="# VIP 5\nPreço: 70K", color=0xFFFFFF),
        ]
        for e in embeds:
            await ctx.send(embed=e)

    # -------- TELLONYM --------
    @commands.command(name="painel_tellonym")
    @commands.has_permissions(administrator=True)
    async def painel_tellonym(self, ctx):
        embed = discord.Embed(
            title="Tellonym",
            description="Envie mensagens anônimas clicando no botão abaixo.",
            color=0xFFFFFF
        )
        await ctx.send(embed=embed, view=TellonymView())

    # -------- PRIMEIRA DAMA --------
    @commands.command()
    async def primeiradama(self, ctx):
        embed = discord.Embed(
            title="Primeira Dama",
            description="Clique no botão para resgatar.",
            color=0xFFFFFF
        )
        await ctx.send(embed=embed, view=PrimeiraDamaView(self.bot))

    # -------- AFK --------
    @commands.hybrid_command(name="afk")
    async def afk(self, ctx, *, motivo="AFK"):
        self.afk_users[ctx.author.id] = motivo
        await ctx.send(f"AFK ativado: **{motivo}**")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if message.author.id in self.afk_users:
            del self.afk_users[message.author.id]

        for user in message.mentions:
            if user.id in self.afk_users:
                await message.channel.send(
                    f"{user.display_name} está AFK: **{self.afk_users[user.id]}**"
                )

    # -------- FUN --------
    @commands.hybrid_command(name="numero")
    async def numero(self, ctx):
        await ctx.send(f"Número escolhido: **{random.randint(1,100)}**")

    @commands.hybrid_command(name="kitar")
    async def kitar(self, ctx):
        frases = [
            "kitou da realidade",
            "kitou porque foi de base",
            "kitou porque desinstalou o Discord",
            "kitou porque é um favelaso subdesenvolvido",
            "kitou porque o Kenjaku mandou",
            "kitou porque... sei lá man, caba só kitou mermo",
            "kit. Ou por. Que a escr. Ita tá u. Ma merd. A",
            "kitou porque a vivi mandou, DITADURA PURA!!!!!!!!!! AHAHSHAHSSHAHAJZJAHAJSJAJA",
            "kitou porque a aura do salva é muito forte",
            "kitou porque a yuna não aparece mais no chat #VoltaYunaSuaCachorra",
            "kitou porque- pera aí, se a água é transparente, porque o mar é azul? 🤔",
            "kitou porque tá muito frio, Ô FRIO DA MOLESTA EIN",
            "kitou porque perdeu o Tung Tung Sahur no Roube um Brainrot",
            ]
        await ctx.send(f"{ctx.author.mention} {random.choice(frases)}")

    # -------- WELCOME --------
    @commands.Cog.listener()
    async def on_member_join(self, member):
        canal = member.guild.get_channel(1410053387558322297)
        if canal:
            await canal.send(f"Bem-vindo(a) {member.mention}!")

# =========================
# SETUP ÚNICO
# =========================
async def setup(bot):
    await bot.add_cog(Utils(bot))
