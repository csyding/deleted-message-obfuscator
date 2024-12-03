import requests
from dotenv import load_dotenv
import os
import json
from string import punctuation
from PIL import Image, ImageDraw, ImageFont



load_dotenv()
API_KEY = os.getenv("API_KEY")


text = input("Type your deleted message: ")
words = text.split()
obfuscated_words = []
for word in words:
    if any(p in word for p in punctuation):
        obfuscated_words.append(word)
        continue  # Python 3
    api_url = 'https://api.api-ninjas.com/v1/thesaurus?word={}'.format(word)
    response = requests.get(api_url, headers={'X-Api-Key': API_KEY})
    if response.status_code == requests.codes.ok:
        print(response.text, type(response.text))
        json_data = json.loads(response.text)
        if json_data["synonyms"]:
            obfuscated_words.append(json_data["synonyms"][0])
        else:
            obfuscated_words.append(word)
    else:
        print("Error:", response.status_code, response.text)

captcha_text = " ".join(obfuscated_words)

# Create a new image
img = Image.new('RGB', (200, 100), color = (73, 109, 137))

# Create a drawing object
draw = ImageDraw.Draw(img)

font_size = 30
# Specify font 
border = 10
im = Image.new("RGB", (1, 1), "white")
font = ImageFont.truetype("/Users/ceciliading/Library/Fonts/carbontype.ttf", font_size)
draw = ImageDraw.Draw(im)
size = draw.textlength(captcha_text, font=font)
width = int(size)
height = font_size
im = Image.new("RGB", (width, height), "white")
draw = ImageDraw.Draw(im)
draw.text((width//2, height//2), captcha_text, anchor='mm', fill="black", font=font)
im.show()
img.save("obfuscated_text.png")

