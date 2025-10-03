import logging

# Configure logging
logging.basicConfig(
    filename="logs/bot.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def log(message):
    """Log messages to file and print to console."""
    logging.info(message)
    print(message)
