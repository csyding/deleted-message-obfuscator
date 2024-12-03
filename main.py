import requests
from dotenv import load_dotenv
import os
import json
from string import punctuation
from PIL import Image, ImageDraw, ImageFont
from groq import Groq

load_dotenv()
API_KEY = os.getenv("API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
PROMPT = os.getenv("PROMPT")

def set_up():
    client = Groq(
        # This is the default and can be omitted
        api_key=GROQ_API_KEY,
    )
    return client

def generate_obfuscated_text(text, client):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": PROMPT + text,
            }
        ],
        model="llama3-8b-8192",
    )
    sentence = chat_completion.choices[0].message.content
    return sentence

def generate_image(sentence):
    # Create a new image
    img = Image.new('RGB', (200, 100), color = (73, 109, 137))

    # Create a drawing object
    draw = ImageDraw.Draw(img)

    font_size = 30
    # Specify font 
    border = 10
    im = Image.new("RGB", (1, 1), "white")
    font = ImageFont.truetype("/static/carbontype.ttf", font_size)
    draw = ImageDraw.Draw(im)
    size = draw.textlength(sentence, font=font)
    width = int(size)
    height = font_size
    im = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(im)
    draw.text((width//2, height//2), sentence, anchor='mm', fill="black", font=font)
    im.show()
    img.save("obfuscated_text.png")

if __name__ == "__main__":
    text = input("Type your deleted message: ")
    client = set_up()
    sentence = generate_obfuscated_text(text, client)
    generate_image(sentence)

