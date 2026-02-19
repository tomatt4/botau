import discord
import aiohttp
import asyncio
from discord.ext import commands

INVITE_LINK = "https://discord.gg/h3nmQEGpq6"
CARGO_ID = 1473883416876421305

async def extrair_texto_da_imagem(image_bytes, api_key):
    url = "https://api.ocr.space/parse/image"
    params = {
        "apikey": api_key,
        "language": "por",
        "OCREngine": 2,
        "isOverlayRequired": False
    }

    data = aiohttp.FormData()
    data.add_field(
        "file",
        image_bytes,
        filename="imagem.png",
        content_type="image/png"
    )

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data, params=params) as resp:
            result = await resp.json()

    if result.get("IsErroredOnProcessing"):
        return None

    parsed = result.get("ParsedResults")
    if not parsed:
        return None

    return parsed[0].get("ParsedText", "").lower()


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

        try:
            await member.send(
                "**Verificação – Primeira Dama**\n\n"
                "Envie um **print do seu perfil** mostrando o link do servidor "
                "(bio, status ou pronome).\n\n"
                "Você tem **2 minutos**."
            )
        except discord.Forbidden:
            await interaction.response.send_message(
                "Ative suas DMs e tente novamente.",
                ephemeral=True
            )
            return

        await interaction.response.send_message(
            "Te mandei uma DM! Envie a imagem lá",
            ephemeral=True
        )

        def check(msg):
            return (
                msg.author.id == member.id
                and isinstance(msg.channel, discord.DMChannel)
                and msg.attachments
            )

        try:
            msg = await self.bot.wait_for("message", timeout=120, check=check)
            attachment = msg.attachments[0]

            # Aceita mais tipos de imagem
            if not attachment.filename.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
                await member.send("Isso não parece uma imagem válida (.png, .jpg, .jpeg, .webp).")
                return

            async with aiohttp.ClientSession() as session:
                async with session.get(attachment.url) as resp:
                    image_bytes = await resp.read()

            texto = await extrair_texto_da_imagem(
                image_bytes,
                self.bot.OCR_API_KEY
            )

            if not texto:
                await member.send("Não consegui ler o texto da imagem. Certifique-se de que o print esteja legível.")
                return

            print(f"OCR retornou: {texto}")  # 🔍 debug

            # Comparação mais tolerante: ignora espaços e quebras de linha
            texto_limpo = texto.replace(" ", "").replace("\n", "")
            link_limpo = INVITE_LINK.split("//")[1].lower()

            if link_limpo in texto_limpo:
                await member.add_roles(cargo)
                await member.send(
                    "**Verificação aprovada!**\n"
                    "Cargo **Primeira Dama** concedido 🎉"
                )
            else:
                await member.send(
                    "Link do servidor não encontrado no print.\n"
                    "Confere se está legível e tente novamente."
                )

        except asyncio.TimeoutError:
            await member.send("Tempo esgotado. Clique no botão novamente.")


class PrimeiraDama(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.OCR_API_KEY = bot.OCR_API_KEY

    @commands.command()
    async def primeiradama(self, ctx):
        embed = discord.Embed(
            title="Cargo Primeira Dama",
            description=(
                "O cargo **Primeira Dama** é um cargo especial para quem ajuda "
                "a divulgar o servidor\n\n"
                "Ao clicar em **Verificar**, o bot vai pedir um print do seu perfil "
                "e analisar automaticamente a imagem para confirmar se o link "
                "do servidor está visível."
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
                "• Coloque o link do servidor no seu perfil\n"
                "• Clique em **Verificar**\n"
                "• Envie o print solicitado na DM"
            ),
            inline=False
        )

        await ctx.send(embed=embed, view=PrimeiraDamaView(self.bot))


async def setup(bot):
    await bot.add_cog(PrimeiraDama(bot))
