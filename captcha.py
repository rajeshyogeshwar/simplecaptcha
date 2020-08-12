import os
import base64
import random
import string
import hashlib

from io import BytesIO
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont


class Captcha(object):

    def __init__(self, **kwargs):

        load_dotenv(override=True)
        self.characters = self._get_characters()
        self.widget_id = self._generate_widget_id()
        self._generate_captcha()

    def _get_characters(self):

        collection = string.ascii_letters + string.digits
        return [collection[random.randint(0, len(collection) - 1)] for i in range(0, 6)]  # noqa: E501

    def _generate_widget_id(self):

        secret_key = os.getenv('SECRET_KEY')
        captcha_text = ''.join(self.characters)
        return hashlib.pbkdf2_hmac('sha256',
                                   captcha_text.encode('utf-8'),
                                   secret_key.encode('utf-8'), 100000).hex()

    def _generate_captcha(self):

        image = Image.new('RGBA', (240, 80), '#EEE')
        draw = ImageDraw.Draw(image)

        for index, character in enumerate(self.characters):
            self._draw_character(draw, character,
                                 ((index * 36) + 10))

        buffered = BytesIO()
        image.save(buffered, format='PNG')
        self.b64_string = str(base64.b64encode(buffered.getvalue()))

    def _draw_character(self, draw, character, margin):

        font = ImageFont.truetype('khmer.ttf', size=random.randint(32, 36))
        fill = '#' + ''.join([string.hexdigits[random.randint(0, 9)]
                              for i in range(0, 3)])
        offset = 10
        draw.text((margin, offset), character, font=font, fill=fill)


def verify_user_captcha(widget_id, input):

    secret_key = os.getenv('SECRET_KEY')
    return hashlib.pbkdf2_hmac(
        'sha256',
        input.encode('utf-8'),
        secret_key.encode('utf-8'),
        100000).hex() == widget_id
