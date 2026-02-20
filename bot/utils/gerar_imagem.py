from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import textwrap
import uuid

def gerar_imagem_tellonym(numero: int, mensagem: str):
    img = Image.open("bot/asset/tellonym_base.png").convert("RGBA")
    draw = ImageDraw.Draw(img)

    # Carregar fontes com tamanho definido
    try:
        fonte_titulo = ImageFont.truetype("arial.ttf", 30)  # título maior
        fonte_texto = ImageFont.truetype("arial.ttf", 24)   # centro/mensagem
        fonte_data = ImageFont.truetype("arial.ttf", 18)    # rodapé
    except:
        # fallback se não encontrar a fonte
        fonte_titulo = ImageFont.load_default()
        fonte_texto = ImageFont.load_default()
        fonte_data = ImageFont.load_default()
    
    largura, altura = img.size

    # 🔝 TOPO
    draw.text(
        (largura // 2, 30),
        f"Mensagem Anônima #{numero}",
        fill="black",
        anchor="mm",
        font=fonte_titulo
    )

    # 💬 CENTRO
    linhas = textwrap.wrap(mensagem, width=40)
    y = altura // 2 - (len(linhas) * 12)  # ajusta vertical melhor

    for linha in linhas:
        draw.text(
            (largura // 2, y),
            linha,
            fill="black",
            anchor="mm",
            font=fonte_texto
        )
        y += 28  # aumenta espaçamento pra texto maior

    # 📅 RODAPÉ
    data = datetime.now().strftime("%d/%m/%Y • %H:%M")
    draw.text(
        (largura // 2, altura - 30),
        data,
        fill="black",
        anchor="mm",
        font=fonte_data
    )

    caminho = f"/tmp/tellonym_{uuid.uuid4().hex}.png"
    img.save(caminho)

    return caminho
