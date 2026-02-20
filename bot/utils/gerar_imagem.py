from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import textwrap
import uuid

def gerar_imagem_tellonym(numero: int, mensagem: str):
    # Abrir a imagem base
    img = Image.open("bot/asset/tellonym_base.png").convert("RGBA")
    draw = ImageDraw.Draw(img)
    largura, altura = img.size

    # Carregar fontes
    try:
        fonte_titulo = ImageFont.truetype("arial.ttf", 100)  # título maior
        fonte_texto = ImageFont.truetype("arial.ttf", 100)   # centro/mensagem
        fonte_data = ImageFont.truetype("arial.ttf", 80)    # rodapé
    except:
        # fallback se não encontrar a fonte
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
    linhas = textwrap.wrap(mensagem, width=40)

    # Calcular altura de cada linha usando textbbox
    bbox = draw.textbbox((0, 0), "A", font=fonte_texto)
    linha_altura = bbox[3] - bbox[1]
    bloco_altura = len(linhas) * (linha_altura + 6)  # 6px de espaçamento

    y = (altura - bloco_altura) // 2  # centraliza verticalmente

    for linha in linhas:
        bbox_linha = draw.textbbox((0, 0), linha, font=fonte_texto)
        largura_texto = bbox_linha[2] - bbox_linha[0]
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

    # Salvar imagem temporária
    caminho = f"/tmp/tellonym_{uuid.uuid4().hex}.png"
    img.save(caminho)

    return caminho
