from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import textwrap
import uuid

def gerar_imagem_tellonym(numero: int, mensagem: str):
    img = Image.open("assets/tellonym_base.png").convert("RGBA")
    draw = ImageDraw.Draw(img)

    fonte_titulo = ImageFont.load_default()
    fonte_texto = ImageFont.load_default()
    fonte_data = ImageFont.load_default()

    largura, altura = img.size

    # 🔝 TOPO
    draw.text(
        (largura // 2, 30),
        f"Mensagem Anônima #{numero}",
        fill="white",
        anchor="mm",
        font=fonte_titulo
    )

    # 💬 CENTRO
    linhas = textwrap.wrap(mensagem, width=40)
    y = altura // 2 - (len(linhas) * 10)

    for linha in linhas:
        draw.text(
            (largura // 2, y),
            linha,
            fill="white",
            anchor="mm",
            font=fonte_texto
        )
        y += 20

    # 📅 RODAPÉ
    data = datetime.now().strftime("%d/%m/%Y • %H:%M")
    draw.text(
        (largura // 2, altura - 30),
        data,
        fill="white",
        anchor="mm",
        font=fonte_data
    )

    caminho = f"/tmp/tellonym_{uuid.uuid4().hex}.png"
    img.save(caminho)

    return caminho
