#!/usr/bin/python

from PIL import Image, ImageDraw, ImageFont
try:
    import board
    import adafruit_ssd1306
    i2c = board.I2C()
    oled = adafruit_ssd1306.SSD1306_I2C(pixels_size[0], pixels_size[1], i2c)
except ImportError:
    oled = None


char_h = 11
rpi_font_poath = "DejaVuSans.ttf"
font = ImageFont.truetype(rpi_font_poath, char_h)
pixels_size = (128, 64)
max_x, max_y = 22, 5
display_lines = [""]

def _display_update():
    """ Show lines on the screen """
    global oled
    image = Image.new("1", pixels_size)
    draw = ImageDraw.Draw(image)
    for y, line in enumerate(display_lines):
        draw.text((0, y*char_h), line, font=font, fill=255, align="left")

    if oled:
        oled.fill(0)
        oled.image(image)
        oled.show()

def add_display_line(text: str):
    """ Add new line with scrolling """
    global display_lines
    # Split line to chunks according to screen width
    text_chunks = [text[i: i+max_x] for i in range(0, len(text), max_x)]
    for text in text_chunks:
        for line in text.split("\n"):
            display_lines.append(line)
            display_lines = display_lines[-max_y:]
    _display_update()

def add_display_tokens(text: str):
    """ Add new tokens with or without extra line break """
    global display_lines
    last_line = display_lines.pop()
    new_line = last_line + text
    add_display_line(new_line)
    
for p in range(20):
    add_display_line(f"{datetime.now().strftime('%H:%M:%S')}: Line-{p}")
    time.sleep(0.2)
