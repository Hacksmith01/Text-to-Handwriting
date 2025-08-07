from PIL import Image, ImageDraw, ImageFont
from fpdf import FPDF
import os

# A4 size in pixels at 300 DPI
WIDTH, HEIGHT = 2480, 3508
MARGIN_X, MARGIN_Y = 150, 150

FONT_PATH = "Myfont-Regular.ttf"  # Path to your handwriting font
FONT_SIZE = 72  # Much bigger for handwriting feel
LINE_SPACING = int(FONT_SIZE * 1.6)

# Load font
font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

# Optional: Load text from file or hardcoded string
try:
    with open("input.txt", "r", encoding="utf-8") as file:
        text = file.read()
except FileNotFoundError:
    text = """Hi Ishan,

This version fixes small font size and spacing issues.
Your handwriting text now fills the page nicely, with realistic spacing and layout.
Keep typing more content to see multiple pages!

- ChatGPT
""" * 10

# Text wrapping based on pixel width
def wrap_text_by_pixels(text, font, max_width):
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        test_line = current_line + (" " if current_line else "") + word
        if font.getlength(test_line) <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return lines

# Prepare pages folder
os.makedirs("pages", exist_ok=True)

# Wrap text
usable_width = WIDTH - 2 * MARGIN_X
usable_height = HEIGHT - 2 * MARGIN_Y
max_lines_per_page = usable_height // LINE_SPACING

wrapped_lines = wrap_text_by_pixels(text, font, usable_width)
pages = [wrapped_lines[i:i+max_lines_per_page] for i in range(0, len(wrapped_lines), max_lines_per_page)]

# Generate images
image_paths = []
for idx, lines in enumerate(pages, start=1):
    img = Image.new("RGB", (WIDTH, HEIGHT), "white")
    draw = ImageDraw.Draw(img)
    y = MARGIN_Y
    for line in lines:
        draw.text((MARGIN_X, y), line, font=font, fill="black")
        y += LINE_SPACING
    path = f"pages/page_{idx}.png"
    img.save(path)
    image_paths.append(path)
    print(f"✅ Saved {path}")

# Generate PDF
pdf = FPDF(unit="pt", format=[WIDTH, HEIGHT])
for img_path in image_paths:
    pdf.add_page()
    pdf.image(img_path, x=0, y=0, w=WIDTH, h=HEIGHT)
pdf.output("output.pdf")
print("📄 PDF generated as output.pdf")
