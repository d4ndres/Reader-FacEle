import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('KEY_GPT')
print(api_key)
