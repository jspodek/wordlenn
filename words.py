# words.py
# loads in a list of all 5 letter words

import logging

logger = logging.getLogger(__name__)

def _get_five_letter_words() -> list[str]:
    filename : str = "words.txt"
    try:
        with open(filename, 'r') as f:
            words : list[str] = f.read().splitlines()
    except FileNotFoundError:
        logger.exception("File words.txt not found. Please make sure you are looking inside the correct directory.")
        raise FileNotFoundError(
            "File \"%s\" not found. Please make sure you are looking inside the correct directory.", filename
        )
    
    logger.debug('words type is %s and is length %s', type(words), len(words))
    return words

logging.info("loading words list")
WORDS_LIST : list[str] = _get_five_letter_words()