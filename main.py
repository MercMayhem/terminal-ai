from src.util import load_openai_api_key

def main():
    openai_key = load_openai_api_key()

if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print("\nExiting...")
