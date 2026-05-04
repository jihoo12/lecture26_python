import tkinter as tk
from tkinter import messagebox
import random

class HangmanGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Hangman GUI")
        self.root.geometry("400x500")

        # 1. Load Words
        self.words = self.load_words("words.txt")
        self.secret_word = random.choice(self.words).lower()
        self.guessed_letters = []
        self.attempts = 6

        # 2. Setup UI Elements
        self.canvas = tk.Canvas(root, width=200, height=200)
        self.canvas.pack(pady=20)
        self.draw_gallows()

        self.word_display = tk.Label(root, text=self.get_display_word(), font=("Courier", 24))
        self.word_display.pack(pady=10)

        self.entry = tk.Entry(root, font=("Arial", 14), width=5)
        self.entry.pack(pady=5)
        self.entry.bind("<Return>", lambda event: self.make_guess()) # Allow 'Enter' key

        self.guess_btn = tk.Button(root, text="Guess Letter", command=self.make_guess)
        self.guess_btn.pack(pady=5)

        self.status_label = tk.Label(root, text=f"Attempts left: {self.attempts}")
        self.status_label.pack(pady=10)

    def load_words(self, filename):
        try:
            with open(filename, "r") as f:
                return [w.strip() for w in f.readlines() if w.strip()]
        except FileNotFoundError:
            return ["tkinter", "interface", "button", "canvas", "window"]

    def get_display_word(self):
        return " ".join([l if l in self.guessed_letters else "_" for l in self.secret_word])

    def draw_gallows(self):
        # Basic Gallows structure
        self.canvas.create_line(20, 180, 180, 180, width=3) # Base
        self.canvas.create_line(50, 180, 50, 20, width=3)   # Pole
        self.canvas.create_line(50, 20, 120, 20, width=3)   # Top
        self.canvas.create_line(120, 20, 120, 40, width=3)  # Rope

    def draw_man(self):
        parts = [
            lambda: self.canvas.create_oval(105, 40, 135, 70, width=3),   # Head
            lambda: self.canvas.create_line(120, 70, 120, 120, width=3),  # Body
            lambda: self.canvas.create_line(120, 80, 100, 100, width=3),  # L Arm
            lambda: self.canvas.create_line(120, 80, 140, 100, width=3),  # R Arm
            lambda: self.canvas.create_line(120, 120, 100, 150, width=3), # L Leg
            lambda: self.canvas.create_line(120, 120, 140, 150, width=3)  # R Leg
        ]
        # Draw the part corresponding to the wrong guess
        index = 5 - self.attempts
        if index < len(parts):
            parts[index]()

    def make_guess(self):
        guess = self.entry.get().lower()
        self.entry.delete(0, tk.END)

        if not guess.isalpha() or len(guess) != 1 or guess in self.guessed_letters:
            return

        self.guessed_letters.append(guess)

        if guess not in self.secret_word:
            self.attempts -= 1
            self.draw_man()
        
        self.update_ui()
        self.check_game_over()

    def update_ui(self):
        self.word_display.config(text=self.get_display_word())
        self.status_label.config(text=f"Attempts left: {self.attempts}")

    def check_game_over(self):
        if "_" not in self.get_display_word():
            messagebox.showinfo("Hangman", f"You won! Word: {self.secret_word}")
            self.root.destroy()
        elif self.attempts <= 0:
            messagebox.showinfo("Hangman", f"Game Over! Word: {self.secret_word}")
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    game = HangmanGUI(root)
    root.mainloop()