from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import textwrap
import uuid

def gerar_imagem_tellonym(numero: int, mensagem: str):
    img = Image.open("bot/asset/tellonym_base.png").convert("RGBA")
    draw = ImageDraw.Draw(img)
    largura, altura = img.size

    # Carrega a fonte do projeto (Roboto renomeada)
    fonte_titulo = ImageFont.truetype("bot/asset/font.ttf", 36)
    fonte_texto = ImageFont.truetype("bot/asset/font.ttf", 28)
    fonte_data   = ImageFont.truetype("bot/asset/font.ttf", 20)

    # 🔝 Título
    draw.text(
        (largura // 2, 40),
        f"Tellonym #{numero}",
        fill="black",
        anchor="mm",
        font=fonte_titulo
    )

    # 💬 Mensagem
    linhas = textwrap.wrap(mensagem, width=40)
    bbox = draw.textbbox((0, 0), "A", font=fonte_texto)
    linha_altura = bbox[3] - bbox[1]
    bloco_altura = len(linhas) * (linha_altura + 6)
    y = (altura - bloco_altura) // 2

    for linha in linhas:
        bbox_linha = draw.textbbox((0, 0), linha, font=fonte_texto)
        largura_texto = bbox_linha[2] - bbox_linha[0]
        x = (largura - largura_texto) // 2
        draw.text((x, y), linha, fill="black", font=fonte_texto)
        y += linha_altura + 6

    # 📅 Rodapé
    data = datetime.now().strftime("%d/%m/%Y • %H:%M")
    draw.text(
        (largura // 2, altura - 40),
        data,
        fill="black",
        anchor="mm",
        font=fonte_data
    )

    caminho = f"/tmp/tellonym_{uuid.uuid4().hex}.png"
    img.save(caminho)
    return caminho
