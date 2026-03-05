# game.py
# A python implementation of a wordle game

import logging
import emojis
import random

log = logging.getLogger(__name__)

## Constants and codes
SUCCESS_CODE = 0
FAIL_CODE = 1
YELLOW_CODE = 2

NUM_LETTERS = 5

log.debug("Importing words list")
import words
log.debug("Successfully imported words list")

class Wordle():
    """
    Docstring for Wordle
    """
    def __init__(self, mystery_word:str='') -> None:
        log.info("Creating Wordle Object")

        self.mystery_word : str = mystery_word

        log.info("No mystery word set, randomly choosing one")
        if self.mystery_word == '':
            self.mystery_word = random.choice(words.WORDS_LIST)

        if (len(self.mystery_word) != NUM_LETTERS) or (not self.mystery_word.isalnum()) or (self.mystery_word not in words.WORDS_LIST):
            log.error("mystery word is not a valid alphanumeric string of length 5 (got %s)", self.mystery_word)
            raise ValueError("mystery word is not a valid alphanumeric string of length 5 (got %s)", self.mystery_word)

        self.current_turn : int = 0
        self.NUM_GUESSES : int = 6

        self.guessed_words : list[str] = []
        self.scores : list[list[int]] = []

    def __str__(self):
        s = f"A Wordle game with mystery word {self.mystery_word} and {self.NUM_GUESSES - self.current_turn} turns left"
        log.debug("__str__ called for %s", s)
        return s
    
    def _score_guess(self, guess : str):
        remaining = list(self.mystery_word)
        score : list[int] = [FAIL_CODE]*NUM_LETTERS

        # First pass only greens
        # this way you won't accidentally count a later green as a yellow
        log.debug("Scoring Greens")
        for index, letter in enumerate(guess):
            if letter == remaining[index]:
                score[index] = SUCCESS_CODE
                remaining[index] = None
        
        log.debug("Scoring Yellows")
        for index, letter in enumerate(guess):
            if score[index] == SUCCESS_CODE:
                continue

            if letter in remaining:
                score[index] = YELLOW_CODE
                remaining.remove(letter)

        self.scores.append(score)
    
    def play_turn(self, guess: str)->int:
        """
        Returns SUCCESS_CODE for successful turn, FAIL_CODE for failed turn
        """
        log.info("Starting turn %s", self.current_turn)

        if (len(guess) != NUM_LETTERS) or (not guess.isalnum()) or (guess not in words.WORDS_LIST):
            log.warning("guess at turn %s is not a valid alphanumeric string of length 5 (got %s)", self.current_turn, guess)
            return FAIL_CODE

        if guess in self.guessed_words:
            log.warning("Attempted %s when previously tried", guess)
            return FAIL_CODE

        self.guessed_words.append(guess)
        log.info("Turn %s complete", self.current_turn)
        return SUCCESS_CODE


    def is_game_won(self)->tuple[bool,int]:
        """
        Returns true if the game is either won or lost, and false otherwise
        If game is won, secondary exit code is SUCCESS_CODE, if lost: FAIL_CODE
        """
        log.info("Checking if Game is over")
        if len(self.scores) == 0:
            log.warning("Attempted to check if game is over before any completed turns")
            return False
        
        log.debug("Check for win condition")
        last_scores = [self.scores[-1][i] == SUCCESS_CODE for i in range(NUM_LETTERS)]
        if all(last_scores):
            log.info("Game was been won")
            return True       
        
        return False
    
    def print_score(self) -> None:
        log.info("Printing Score")
        def code_to_emoji(code):
            if code == SUCCESS_CODE:
                return ":green_square:"
            elif code == YELLOW_CODE:
                return ":yellow_square:"
            elif code == FAIL_CODE:
                return ":black_large_square:"
            
        log.info("converting to emojis")
        if len(self.scores) == 0:
            log.warning("attempted to output scores with none specified")
            return
        

        outscore: str = " ".join(list(map(code_to_emoji, self.scores[-1])))

        print(emojis.encode(outscore.strip()))
    
    def game_loop(self):
        log.info("Begining Game Loop")

        while self.current_turn < 6:
            log.debug("Getting guess from stdin")
            guess = input(f"Turn {self.current_turn+1}\nEnter your guess: ")

            result = self.play_turn(guess)
            if result is FAIL_CODE:
                log.info("Failed to play turn")
                continue

            log.info("Calculating Score")
            self._score_guess(guess)

            log.info("Printing Guess")
            self.print_score()


            won_game : bool = self.is_game_won()
            if won_game:
                print(f"Congradulations, you won in {self.current_turn + 1} turn(s)")
                print(f"The Mystery word was {self.mystery_word}")
                return


            self.current_turn += 1
        print(f"Sorry, you lost. The mystery word was {self.mystery_word}")


                
if __name__ == "__main__":

    log.debug("Getting starting word from stdin")
    starting_word = input("Enter Starting Word: ").lower()
    log.debug("Succesfully got starting word")
    
    log.info("Initializing game")
    game = Wordle(starting_word)
    log.info("Game is initialized: %s", game)