import requests
from dotenv import load_dotenv
import os
import json
from string import punctuation


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

print(" ".join(obfuscated_words))