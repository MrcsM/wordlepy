from wordle_word_list import words as word_list
from random import randint
from enum import Enum

class WordleGuess(Enum):
    INVALID = 0
    LOSS = 1
    WIN = 2
    INCORRECT = 3

class WordlePosition(Enum):
    CORRECT = 0
    INCORRECT = 1
    WRONG_SPOT = 2

class WordleGame:
    valid_word_list = []
    valid_guesses = []

    word = ""

    guesses = []
    max_guesses = 5
    
    letter_placements = {}
    debug = False

    def __init__(self, words = word_list, debug = False):
        self.valid_word_list = words.copy()
        self.valid_guesses = words.copy()

        self.word = self.get_random_word()

        if debug:
            print(f"[DEBUG] Word: {self.word}")

        self.guesses = []
        self.max_guesses = 5

        # this should be a list of dictionaries, where each dictionary represents the letter placements for a guess
        # for example, if the word is "hello" and the FIRST guess is "adieu", then the letter placements would be:
        # [1: {CORRECT: [(0, 'h')], INCORRECT: [(1, 'e'), (2, 'l'), (3, 'l'), (4, 'o')}]
        self.letter_placements = {}
        self.debug = debug

    def _update_letter_placements(self, current_guess, guess_string):
        if self.debug:
            print(f"[DEBUG] Guess {current_guess}: {guess_string}")

        # initialize letter placements for current guess
        self.letter_placements[current_guess-1] = {
            WordlePosition.CORRECT.name: [],
            WordlePosition.INCORRECT.name: [],
            WordlePosition.WRONG_SPOT.name: []
        }

        for i, letter in enumerate(guess_string):
            if letter == self.word[i]:
                self.letter_placements[current_guess-1][WordlePosition.CORRECT.name].append((i, letter))
            elif letter in self.word:
                self.letter_placements[current_guess-1][WordlePosition.WRONG_SPOT.name].append((i, letter))
            else:
                # put this back to appending (i, letter) for positioning later
                self.letter_placements[current_guess-1][WordlePosition.INCORRECT.name].append(letter)
        
    # this method shouldn't be left in here, but it's nice to have the logic for the bot guessing words later
    def _remove_invalid_words(self):
        removed_words = []
        counter = 0

        if self.debug:
            print(f"[DEBUG] Letter Placements: {self.letter_placements}")

        for word in self.valid_word_list:
            for i, letter in enumerate(word):
                # will need to check for tuple later
                # remove any words that have letters that are incorrect
                if letter in self.letter_placements[len(self.guesses)-1][WordlePosition.INCORRECT.name]:
                    removed_words.append(word)
                    break

                # remove any words that have letters in the same index as previous guesses which were determined to be in the wrong spot
                if (i, letter) in self.letter_placements[len(self.guesses)-1][WordlePosition.WRONG_SPOT.name]:
                    removed_words.append(word)
                    break

                # keep any words that have letters in the same index as previous guesses which were determined to be correct
                if (i, letter) in self.letter_placements[len(self.guesses)-1][WordlePosition.CORRECT.name]:
                    continue

        for word in removed_words:
            if word in self.valid_word_list:
                self.valid_word_list.remove(word)
                counter += 1

        if self.debug:
            print(f"[DEBUG] Removed {counter} words ({len(self.valid_word_list)} remaining)")

    def get_random_word(self):
        return self.valid_word_list[randint(0, len(self.valid_word_list) - 1)]
    
    def is_game_running(self):
        return len(self.guesses) < self.max_guesses and self.word not in self.guesses
    
    def guess(self, guess):
        if len(guess) != 5 or guess in self.guesses or guess not in self.valid_guesses:
            return WordleGuess.INVALID, {}
        
        self.guesses.append(guess)

        self._update_letter_placements(len(self.guesses), guess)

        if guess == self.word:
            return WordleGuess.WIN, self.letter_placements[len(self.guesses)-1]

        if (self.guesses == self.max_guesses and guess != self.word):
            return WordleGuess.LOSS, self.letter_placements[len(self.guesses)-1]
        
        self._remove_invalid_words()
        
        for i, guess in enumerate(self.guesses):
            for letter in guess:
                for tup in self.letter_placements[i][WordlePosition.CORRECT.name]:
                    if letter == tup[1]:
                        print(f"{letter.capitalize()} (C)", end=" ")
                        break
                
                for tup in self.letter_placements[i][WordlePosition.WRONG_SPOT.name]:
                    if letter == tup[1]:
                        print(f"{letter.capitalize()} (W)", end=" ")
                        break

                # will need to check for tuple later
                if letter in self.letter_placements[i][WordlePosition.INCORRECT.name]:
                    print(f"{letter.capitalize()} (I)", end=" ")

            print()

        print(f"Guesses Left: {5 - len(self.guesses)}")

        return WordleGuess.INCORRECT, self.letter_placements[len(self.guesses)-1]
