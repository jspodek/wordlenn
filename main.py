import logging
import os
import datetime

## Initialize Logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename=os.path.join("logs", "{}.log".format(datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S"))),
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M:%S",
    level="DEBUG"
)
log = logging.getLogger(__name__)

log.debug('Importing Wordle')
import wordle

def main():
    pass

if __name__ == "__main__":
    game = wordle.Wordle('apple')

    game.turn('banan')