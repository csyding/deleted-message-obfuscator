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


client = Groq(
    # This is the default and can be omitted
    api_key=GROQ_API_KEY,
)

text = input("Type your deleted message: ")

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "generate just one synonymous (and slightly more awkward) sentence for this: " + text + ". please do not include any other text and please try to keep it short."
        }
    ],
    model="llama3-8b-8192",
)
sentence = chat_completion.choices[0].message.content
print(sentence)

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
size = draw.textlength(sentence, font=font)
width = int(size)
height = font_size
im = Image.new("RGB", (width, height), "white")
draw = ImageDraw.Draw(im)
draw.text((width//2, height//2), sentence, anchor='mm', fill="black", font=font)
im.show()
img.save("obfuscated_text.png")

