from wordle_game import WordleGame, WordleGuess

def main():
    game = WordleGame()

    while game.is_game_running():
        guess = input("Enter your guess: ")
        result, letter_placement = game.guess(guess)
        print(letter_placement)
        if result == WordleGuess.WIN:
            print(f"You won on guess {len(game.guesses)}!")
        elif result == WordleGuess.LOSS:
            print(f"You lose! The word was {game.word}")
        elif result == WordleGuess.INVALID:
            print("Invalid guess. Please try again.")
        print("-------------------------------------")

if __name__ == "__main__":
    main()