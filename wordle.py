# game.py
# A python implementation of a wordle game

import logging

log = logging.getLogger(__name__)


log.debug("Importing words list")
import words
log.debug("Successfully imported words list")

class Wordle():
    """
    Docstring for Wordle
    """
    def __init__(self, mystery_word:str) -> None:
        log.info("Creating Wordle Object")

        self.words_list : list[str] = words.WORDS_LIST

        self.mystery_word : str = mystery_word

        if (len(self.mystery_word) != 5) or (not self.mystery_word.isalnum()) or (self.mystery_word not in self.words_list):
            log.error("mystery word is not a valid alphanumeric string of length 5 (got %s)", self.mystery_word)
            raise ValueError("mystery word is not a valid alphanumeric string of length 5 (got %s)", self.mystery_word)

        self.current_guess : int = 0
        self.NUM_GUESSES : int = 6

        self.guessed_words : list[str] = []

    def __str__(self):
        s = f"A Wordle game with mystery word {self.mystery_word} and {self.NUM_GUESSES - self.current_guess} turns left"
        log.debug("__str__ called for %s", s)
        return s
    
    def turn(self, guess: str)->None:
        if (len(guess) != 5) or (not guess.isalnum()) or (guess not in self.words_list):
            log.error("guess at turn %s is not a valid alphanumeric string of length 5 (got %s)", self.current_guess, guess)
            raise ValueError("guess at turn %s is not a valid alphanumeric string of length 5 (got %s)", self.current_guess, guess)

        if guess in self.guessed_words:
            log.warning("Attempted %s when previously tried", guess)
            return


        
        self.guessed_words.append(guess)

    def game_over(self):
        pass
        
if __name__ == "__main__":
    log.debug("Getting starting word from stdin")
    starting_word = input("Enter Starting Word: ").lower()
    log.debug("Succesfully got starting word")
    
    log.info("Initializing game")
    game = Wordle(starting_word)
    log.info("Game is initialized: %s", game)