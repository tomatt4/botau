from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import textwrap
import uuid

def gerar_imagem_tellonym(numero: int, mensagem: str):
    # 🔹 Abrir a imagem base
    img = Image.open("bot/asset/tellonym_base.png").convert("RGBA")
    draw = ImageDraw.Draw(img)
    largura, altura = img.size

    # 🔹 Carregar fontes com tamanho definido
    try:
        fonte_titulo = ImageFont.truetype("arial.ttf", 36)  # título maior
        fonte_texto = ImageFont.truetype("arial.ttf", 28)   # mensagem
        fonte_data = ImageFont.truetype("arial.ttf", 20)    # rodapé
    except:
        # fallback se a fonte não existir
        fonte_titulo = ImageFont.load_default()
        fonte_texto = ImageFont.load_default()
        fonte_data = ImageFont.load_default()

    # 🔝 TOPO - Título
    draw.text(
        (largura // 2, 40),
        f"Mensagem Anônima #{numero}",
        fill="black",
        anchor="mm",
        font=fonte_titulo
    )

    # 💬 CENTRO - Mensagem
    # Quebra linhas e calcula altura total
    linhas = textwrap.wrap(mensagem, width=40)
    # Com textsize:
    linha_altura = draw.textsize("A", font=fonte_texto)[1]
    # Ou, de forma mais moderna com textbbox:
    linha_altura = draw.textbbox((0,0), "A", font=fonte_texto)[3]  # altura = bottom - top
    bloco_altura = len(linhas) * (linha_altura + 6)  # 6px espaçamento

    y = (altura - bloco_altura) // 2  # centraliza verticalmente

    for linha in linhas:
        largura_texto, _ = draw.textsize(linha, font=fonte_texto)
        x = (largura - largura_texto) // 2  # centraliza horizontalmente
        draw.text((x, y), linha, fill="black", font=fonte_texto)
        y += linha_altura + 6

    # 📅 RODAPÉ
    data = datetime.now().strftime("%d/%m/%Y • %H:%M")
    draw.text(
        (largura // 2, altura - 40),
        data,
        fill="black",
        anchor="mm",
        font=fonte_data
    )

    # 🔹 Salvar imagem temporária
    caminho = f"/tmp/tellonym_{uuid.uuid4().hex}.png"
    img.save(caminho)

    return caminho
