import os

from dotenv import load_dotenv


load_dotenv()


def main():
    app_name = os.getenv("APP_NAME")
    environment = os.getenv("APP_ENV")

    print(f"{app_name} is starting...")
    print(f"Environment: {environment}")


if __name__ == "__main__":
    main()