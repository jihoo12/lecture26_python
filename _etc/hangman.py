import random
import os

def load_words(filename):
    #Reads words from a text file and returns a list.
    try:
        with open(filename, "r") as file:
            word_list = file.read().splitlines()
            return [word for word in word_list if word.strip()]
    except FileNotFoundError:
        print(f"Error: '{filename}' not found. Using fallback list.")
        return ['apple', 'banana', 'orange']

def play_hangman():
    words = load_words("words.txt")
    secret_word = random.choice(words).lower()
    guessed_letters = []
    attempts = 6
    
    print("--- Welcome to Hangman ---")
    
    while attempts > 0:
        display_word = "".join([l if l in guessed_letters else "_" for l in secret_word])
        
        print(f"\nWord: {' '.join(display_word)}")
        print(f"Attempts left: {attempts}")

        if "_" not in display_word:
            print(f"Winner! You found the word: {secret_word}")
            break

        guess = input("Guess a letter: ").lower()

        if len(guess) != 1 or not guess.isalpha():
            continue
        if guess in guessed_letters:
            print("Already tried that!")
            continue

        guessed_letters.append(guess)

        if guess not in secret_word:
            attempts -= 1
            print("Incorrect!")

    else:
        print(f"\nGame Over. The word was: {secret_word}")

if __name__ == "__main__":
    play_hangman()