import random
class Hangman:
    MAX_TRY = 7
    MASK_CHAR = '_'
    RIGHT = 1
    WRONG = 0
    EXIST = -1
    WIN = 1
    LOOSE = 0
    CONTINUE = -1
    def __init__(self, word_list):
        self.word = random.choice(word_list).upper()
        self.display_word = Hangman.MASK_CHAR * len(self.word)
        self.num_try = 0
    def check_letter(self, letter):
        letter = letter.upper()
        if self.word.count(letter) > 0: 
            # 있는 문자이면 display_word에서 위치를 찾아 수정
            for i in range(len(self.word)):
                if self.word[i] == letter:
                    self.display_word = self.display_word[:i] + letter + self.display_word[i+1:]
            return Hangman.RIGHT
        else:
            self.num_try += 1
            return Hangman.WRONG
    def is_win(self):
        # 이겼을 때
        if self.display_word.count(Hangman.MASK_CHAR) == 0:
            return Hangman.WIN
        # 졌을 때
        elif self.num_try >= Hangman.MAX_TRY:
            return Hangman.LOOSE

        return Hangman.CONTINUE