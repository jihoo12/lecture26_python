import random
class Hangman:
    MASK_CHAR = ' '
    def __init__(self,word_list):
        self.word = random.choice(word_list)
        self.display_word = Hangman.MASK_CHAR * len(self.word)
        self.num_try = 0
    def check_letter(self,letter):
        letter = letter.upper()
        if self.word.count(letter) > 0:
            for i in range(len(self.word)):
                self.display_word = self.display_word[:i] + letter + self.display_word[i+1:]
            return Hangman.Right
    def is_win(self,letter):
        if self.display_word.count(Hangman.MASK_CHAR) == 0:
            return Hangman.WIN
        pass

