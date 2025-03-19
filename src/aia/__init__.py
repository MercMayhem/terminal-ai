from .util import load_openai_api_key
from .workflow import start_workflow

def run():
    try:
        openai_key = load_openai_api_key()
        start_workflow(key=openai_key)

    except KeyboardInterrupt:
        print("\nExiting...")

