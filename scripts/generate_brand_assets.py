from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
CANVAS_FONTS = Path("/Users/a1-6/.codex/skills/canvas-design/canvas-fonts")

BG = "#f4efe4"
INK = "#111215"
RED = "#a2182a"
STEEL = "#98a4b3"
LIGHT = "#f7f2e7"


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(CANVAS_FONTS / name), size=size)


DISPLAY = font("BricolageGrotesque-Bold.ttf", 152)
DISPLAY_SMALL = font("BricolageGrotesque-Bold.ttf", 60)
MONO = font("GeistMono-Regular.ttf", 30)
MONO_SMALL = font("GeistMono-Regular.ttf", 24)


def draw_grid(draw: ImageDraw.ImageDraw, width: int, height: int, step: int, color: str, alpha: int) -> None:
    line = color + f"{alpha:02x}"
    for x in range(0, width + 1, step):
      draw.line((x, 0, x, height), fill=line, width=1)
    for y in range(0, height + 1, step):
      draw.line((0, y, width, y), fill=line, width=1)


def add_soft_glow(base: Image.Image, box: tuple[int, int, int, int], color: tuple[int, int, int, int], blur: int) -> None:
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    overlay = ImageDraw.Draw(layer)
    overlay.ellipse(box, fill=color)
    layer = layer.filter(ImageFilter.GaussianBlur(blur))
    base.alpha_composite(layer)


def draw_mark(draw: ImageDraw.ImageDraw, x: int, y: int, size: int) -> None:
    pad = int(size * 0.12)
    inner = size - pad * 2
    draw.rounded_rectangle((x, y, x + size, y + size), radius=int(size * 0.18), fill=INK)
    draw.rounded_rectangle(
        (x + pad, y + pad, x + size - pad, y + size - pad),
        radius=int(size * 0.13),
        outline=(247, 242, 231, 48),
        width=max(2, size // 50),
    )
    draw.line((x + size // 2, y + pad, x + size // 2, y + size - pad), fill=(247, 242, 231, 28), width=max(1, size // 100))
    draw.line((x + pad, y + size // 2, x + size - pad, y + size // 2), fill=(247, 242, 231, 28), width=max(1, size // 100))
    stroke = int(size * 0.12)
    left = x + int(size * 0.28)
    right = x + int(size * 0.72)
    top = y + int(size * 0.25)
    mid = y + int(size * 0.50)
    bottom = y + int(size * 0.75)
    draw.line((left, top, left, bottom), fill=LIGHT, width=stroke)
    draw.line((right, top, right, bottom), fill=LIGHT, width=stroke)
    draw.line((left, mid, right, mid), fill=LIGHT, width=stroke)
    draw.line((right - int(size * 0.08), top, x + size - int(size * 0.15), mid), fill=RED, width=stroke)
    draw.line((x + size - int(size * 0.15), mid, x + size - int(size * 0.15), bottom), fill=RED, width=stroke)
    accent = int(size * 0.16)
    draw.rectangle((x + size - pad - accent, y + pad, x + size - pad, y + pad + accent), fill=RED)


def create_board(width: int, height: int) -> Image.Image:
    img = Image.new("RGBA", (width, height), BG)
    draw = ImageDraw.Draw(img)

    add_soft_glow(img, (width - 420, -90, width + 50, 280), (162, 24, 42, 54), 60)
    add_soft_glow(img, (-160, height - 320, 260, height + 100), (16, 17, 20, 26), 60)

    draw_grid(draw, width, height, max(56, width // 18), "#101114", 12)

    inset = 44
    draw.rounded_rectangle((inset, inset, width - inset, height - inset), radius=34, outline=(16, 17, 20, 24), width=2)
    draw.line((width * 0.58, inset, width * 0.58, height - inset), fill=(16, 17, 20, 28), width=2)
    draw.line((inset, int(height * 0.54), width - inset, int(height * 0.54)), fill=(16, 17, 20, 24), width=2)
    return img


def save_brand_board() -> None:
    width, height = 1600, 900
    img = create_board(width, height)
    draw = ImageDraw.Draw(img)

    draw_mark(draw, 88, 88, 260)
    draw.text((392, 116), "Hans", font=DISPLAY, fill=INK)
    draw.text((392, 258), "Niemann", font=DISPLAY, fill=INK)
    draw.text((394, 418), "RATING / TIMELINE / FACTS", font=MONO, fill="#5d646c")

    draw.rounded_rectangle((88, 560, 1512, 816), radius=32, fill=(255, 255, 255, 170), outline=(16, 17, 20, 24), width=2)
    draw.text((128, 610), "ENDGAME TENSION", font=MONO_SMALL, fill=RED)
    draw.text((128, 660), "A cold board identity for a high-pressure modern chess profile.", font=DISPLAY_SMALL, fill=INK)

    draw.line((1240, 86, 1480, 326), fill=RED, width=10)
    draw.line((1268, 86, 1508, 326), fill=(16, 17, 20, 70), width=4)

    img.save(ASSETS / "brand-composition.png")


def save_og_image() -> None:
    width, height = 1200, 630
    img = create_board(width, height)
    draw = ImageDraw.Draw(img)

    draw.rounded_rectangle((44, 44, width - 44, height - 44), radius=32, fill=(255, 255, 255, 122))
    draw_mark(draw, 78, 86, 190)
    draw.text((320, 110), "Hans Niemann", font=font("BricolageGrotesque-Bold.ttf", 92), fill=INK)
    draw.text((324, 232), "Current rating, career timeline, and key facts.", font=font("BricolageGrotesque-Bold.ttf", 40), fill=INK)
    draw.text((324, 302), "FIDE APR 2026 / 2728 STANDARD / WORLD 20", font=MONO_SMALL, fill="#5d646c")
    draw.line((78, 520, 1122, 520), fill=(16, 17, 20, 24), width=2)
    draw.text((78, 544), "hans-niemann.lol", font=MONO_SMALL, fill=RED)
    img.save(ASSETS / "og-image.png")


def save_icon(size: int, filename: str) -> None:
    img = Image.new("RGBA", (size, size), BG)
    draw = ImageDraw.Draw(img)
    draw_mark(draw, 0, 0, size)
    img.save(ASSETS / filename)


def main() -> None:
    ASSETS.mkdir(exist_ok=True)
    save_brand_board()
    save_og_image()
    save_icon(180, "apple-touch-icon.png")
    save_icon(32, "favicon-32x32.png")
    save_icon(16, "favicon-16x16.png")


if __name__ == "__main__":
    main()
