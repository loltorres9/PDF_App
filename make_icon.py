"""Erzeugt app.ico — das Symbol der Exe, des Startmenü-Eintrags und des Fensters.

Das Icon liegt fertig im Repository; dieses Skript ist der Bauplan dazu, damit
es sich nachvollziehbar ändern lässt statt in einem Grafikprogramm zu leben:

    python make_icon.py

Braucht Pillow, sonst nichts. Für den Build der Exe wird es nicht ausgeführt.
"""

from __future__ import annotations

from PIL import Image, ImageDraw

SIZE = 1024  # Vorlage; die .ico-Größen werden daraus verkleinert
ICO_SIZES = [16, 24, 32, 48, 64, 128, 256]

RED_TOP = (196, 58, 47)
RED_BOTTOM = (140, 30, 24)
PAPER = (255, 255, 255)
PAPER_EDGE = (214, 214, 218)
INK = (150, 36, 29)


def _rounded_background() -> Image.Image:
    """Abgerundetes Quadrat mit senkrechtem Farbverlauf."""
    gradient = Image.new("RGB", (1, SIZE))
    for y in range(SIZE):
        t = y / (SIZE - 1)
        gradient.putpixel(
            (0, y),
            tuple(round(a + (b - a) * t) for a, b in zip(RED_TOP, RED_BOTTOM)),
        )
    gradient = gradient.resize((SIZE, SIZE))

    mask = Image.new("L", (SIZE, SIZE), 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        (0, 0, SIZE - 1, SIZE - 1), radius=int(SIZE * 0.22), fill=255
    )
    background = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    background.paste(gradient, (0, 0), mask)
    return background


def _page(width: int, height: int, fold: int) -> Image.Image:
    """Ein Blatt Papier mit umgeknickter Ecke oben rechts."""
    page = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(page)
    body = [
        (0, 0),
        (width - fold, 0),
        (width - 1, fold),
        (width - 1, height - 1),
        (0, height - 1),
    ]
    draw.polygon(body, fill=PAPER, outline=PAPER_EDGE)
    # Der Knick selbst — etwas dunkler, damit er auch klein sichtbar bleibt.
    draw.polygon(
        [(width - fold, 0), (width - 1, fold), (width - fold, fold)],
        fill=(232, 232, 236),
        outline=PAPER_EDGE,
    )
    return page


def _arrow(size: int) -> Image.Image:
    """Pfeil nach unten — das Zusammenführen der Blätter zu einer Datei."""
    arrow = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(arrow)
    draw.ellipse((0, 0, size - 1, size - 1), fill=INK, outline=PAPER, width=size // 14)
    shaft = size * 0.13
    draw.rectangle(
        (size / 2 - shaft, size * 0.24, size / 2 + shaft, size * 0.58), fill=PAPER
    )
    draw.polygon(
        [
            (size * 0.27, size * 0.52),
            (size * 0.73, size * 0.52),
            (size / 2, size * 0.80),
        ],
        fill=PAPER,
    )
    return arrow


def build() -> Image.Image:
    icon = _rounded_background()

    # Bewusst wenige, große Formen: bei 16 Pixeln überlebt nichts Feineres.
    back = _page(360, 470, 95).rotate(9, expand=True, resample=Image.BICUBIC)
    front = _page(360, 470, 95).rotate(-6, expand=True, resample=Image.BICUBIC)
    icon.alpha_composite(back, (170, 190))
    icon.alpha_composite(front, (320, 250))

    arrow = _arrow(330)
    icon.alpha_composite(arrow, (SIZE - 400, SIZE - 400))
    return icon


if __name__ == "__main__":
    image = build()
    image.save("app.ico", sizes=[(n, n) for n in ICO_SIZES])
    image.resize((256, 256), Image.LANCZOS).save("app.png")
    print("app.ico und app.png geschrieben")
