import uuid
import textwrap
from PIL import Image, ImageDraw, ImageFont
import base64
from io import BytesIO

class MemeGenerator:
    def make_unique_filename(self, source):
        filename, _, extension = source.rpartition('.')
        return f'{filename}_{uuid.uuid4()}.{extension}'

    def create_meme(self, image_path, top_text, bottom_text, font_size):
        return self.generate_meme(image_path, top_text, bottom_text, font_size, save=True)

    def preview_image(self, image_path, top_text, bottom_text, font_size):
        return self.generate_meme(image_path, top_text, bottom_text, font_size, save=False)

    def generate_meme(self, image_path, top_text, bottom_text, font_size, save):
        font_path = 'ofont.ru_Impact.ttf'
        img = Image.open(image_path)
        draw = ImageDraw.Draw(img)
        image_width, image_height = img.size
        stroke_width = 5

        # load font
        font = ImageFont.truetype(font=font_path, size=int(font_size))

        # convert text to uppercase
        top_text = top_text.upper()
        bottom_text = bottom_text.upper()

        # text wrapping
        left, top, right, bottom = font.getbbox('A')
        char_width = right - left
        char_height = bottom - top
        chars_per_line = image_width // char_width
        top_lines = textwrap.wrap(top_text, width=chars_per_line)
        bottom_lines = textwrap.wrap(bottom_text, width=chars_per_line)

        # draw top lines
        y = 0
        for line in top_lines:
            left, top, right, bottom = font.getbbox(line)
            line_width = right - left
            line_height = bottom - top
            x = (image_width - line_width) / 2
            draw.text((x, y), line, fill='white', font=font, stroke_width=stroke_width, stroke_fill='black')
            y += line_height + 7

        # draw bottom lines
        y = image_height - char_height * len(bottom_lines) - 25
        for line in bottom_lines:
            left, top, right, bottom = font.getbbox(line)
            line_width = right - left
            line_height = bottom - top
            x = (image_width - line_width) / 2
            draw.text((x, y), line, fill='white', font=font, stroke_width=stroke_width, stroke_fill='black')
            y += line_height + 7

        if save:
            filename = self.make_unique_filename(image_path)
            img.save(filename)
            return filename
        else:
            buffered = BytesIO()
            img.save(buffered, format="PNG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
            return img_base64