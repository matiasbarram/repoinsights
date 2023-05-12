from services.extract_service.config import GHToken
from loguru import logger


def main():
    tokens = GHToken().get_public_tokens(many=True)
    for token, calls in tokens:
        logger.info(f"{token[-10:]}: {calls}")


if __name__ == "__main__":
    main()
