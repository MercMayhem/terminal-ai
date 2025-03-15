from .util import load_openai_api_key

def run():
    try:
        openai_key = load_openai_api_key()

    except KeyboardInterrupt:
        print("\nExiting...")

