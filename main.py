import requests
from dotenv import load_dotenv
import os
from string import punctuation
from PIL import Image, ImageDraw, ImageFont
from groq import Groq
from captcha.image import ImageCaptcha
import io


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
    sentence = str(sentence)
    custom_fonts = ['/static/carbontype.ttf']
    captcha = ImageCaptcha(fonts=custom_fonts, width=20*len(sentence), height=100, font_sizes=[20, 10])
    data = captcha.generate_image(sentence)
    return data

if __name__ == "__main__":
    text = input("Type your deleted message: ")
    client = set_up()
    sentence = generate_obfuscated_text(text, client)
    
    image = generate_image(sentence)
    image.show()
    image.save("obfuscated_text.png")

