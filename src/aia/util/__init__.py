import os
import dotenv
from pathlib import Path
import requests
from typing import Optional

def load_openai_api_key() -> str:

    # Create .env in grandparent directory of project (if it doesn't exist)
    env_file = Path(__file__).resolve().parent.parent / ".env"
    env_file.touch(mode=0o600, exist_ok=True)

    # Load .env
    dotenv.load_dotenv(env_file)

    openai_key = os.environ.get("OPENAI_KEY")

    # Place OpenAI key in .env if not present also check validity
    valid: Optional[bool] = None
    while not openai_key or not (valid := is_openai_key_valid(openai_key)):
        if not valid and valid is not None:
            print("Invalid api key: Unauthorized")
        openai_key = input("Enter OpenAI key: ")

    dotenv.set_key(env_file, key_to_set="OPENAI_KEY", value_to_set=openai_key)

    return openai_key

# Test if key is valid by querying test endpoint
def is_openai_key_valid(key: str) -> bool:
    test_endpoint = "https://api.openai.com/v1/models"
    test_headers = {
        "Authorization": f"Bearer {key}"
    }

    response = requests.get(test_endpoint, headers=test_headers)

    if response.status_code == 401:
        return False
    return True
