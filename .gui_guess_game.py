import tkinter as tk
from tkinter import messagebox
import random
import os
import simpleaudio as sa

# Load sounds
def play_sound(file):
    try:
        wave_obj = sa.WaveObject.from_wave_file(file)
        wave_obj.play()
    except Exception as e:
        print("Sound error:", e)

# Scoreboard and high score logic
def save_score(name, attempts):
    with open("scoreboard.txt", "a") as file:
        file.write(f"{name}: {attempts} attempts\n")

def get_high_score():
    if os.path.exists("highscore.txt"):
        with open("highscore.txt", "r") as file:
            line = file.readline().strip()
            if line:
                name, score = line.split(":")
                return name, int(score)
    return None, float("inf")

def update_high_score(name, attempts):
    _, current_high_score = get_high_score()
    if attempts < current_high_score:
        with open("highscore.txt", "w") as file:
            file.write(f"{name}:{attempts}")

def get_scoreboard():
    if os.path.exists("scoreboard.txt"):
        with open("scoreboard.txt", "r") as file:
            return file.read().strip()
    return "No scores yet."

# GUI Game Logic
class NumberGuessingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🎯 Number Guessing Game")
        self.root.configure(bg="skyblue")

        self.name = ""
        self.difficulty = ""
        self.secret_number = 0
        self.max_number = 20
        self.attempts = 0

        self.create_widgets()

    def create_widgets(self):
        # Player Name
        tk.Label(self.root, text="Enter your name:", font=("Helvetica", 14, "bold"), bg="skyblue").pack(pady=10)
        self.name_entry = tk.Entry(self.root, font=("Helvetica", 14))
        self.name_entry.pack(pady=5)

        # Difficulty
        tk.Label(self.root, text="Select Difficulty:", font=("Helvetica", 14, "bold"), bg="skyblue").pack(pady=10)
        self.difficulty_var = tk.StringVar()

        difficulty_frame = tk.Frame(self.root, bg="skyblue")
        difficulty_frame.pack(pady=5)

        tk.Radiobutton(difficulty_frame, text="Easy (1-20)", variable=self.difficulty_var, value="Easy", bg="skyblue", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(difficulty_frame, text="Medium (1-50)", variable=self.difficulty_var, value="Medium", bg="skyblue", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(difficulty_frame, text="Hard (1-100)", variable=self.difficulty_var, value="Hard", bg="skyblue", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=5)

        # Start Button
        self.start_button = tk.Button(self.root, text="Start Game", command=self.start_game, font=("Helvetica", 14, "bold"))
        self.start_button.pack(pady=15)

        # Game Interface
        self.guess_label = tk.Label(self.root, text="", font=("Helvetica", 14), bg="skyblue")
        self.guess_entry = tk.Entry(self.root, font=("Helvetica", 14))
        self.submit_button = tk.Button(self.root, text="Submit Guess", command=self.check_guess, font=("Helvetica", 14, "bold"))
        self.feedback_label = tk.Label(self.root, text="", font=("Helvetica", 14, "bold"), bg="skyblue")

        self.play_again_button = tk.Button(self.root, text="Play Again", font=("Helvetica", 12, "bold"), command=self.play_again)
        self.reset_button = tk.Button(self.root, text="Reset Game", font=("Helvetica", 12, "bold"), command=self.reset_game)

        # Score Display
        self.scoreboard_frame = tk.Frame(self.root, bg="black", padx=10, pady=10)
        self.high_score_label = tk.Label(self.scoreboard_frame, text="", font=("Helvetica", 12, "bold"), bg="black", fg="white")
        self.scoreboard_label = tk.Label(self.scoreboard_frame, text="", font=("Helvetica", 11), bg="black", fg="white", justify=tk.LEFT)

    def start_game(self):
        self.name = self.name_entry.get().strip()
        self.difficulty = self.difficulty_var.get()

        if not self.name or not self.difficulty:
            messagebox.showwarning("Input Required", "Please enter your name and select difficulty.")
            return

        if self.difficulty == "Easy":
            self.max_number = 20
        elif self.difficulty == "Medium":
            self.max_number = 50
        elif self.difficulty == "Hard":
            self.max_number = 100

        self.secret_number = random.randint(1, self.max_number)
        self.attempts = 0
        play_sound("start.wav")

        self.name_entry.pack_forget()
        self.start_button.pack_forget()

        self.guess_label.config(text=f"Guess a number between 1 and {self.max_number}:")
        self.guess_label.pack(pady=10)
        self.guess_entry.pack(pady=5)
        self.submit_button.pack(pady=5)
        self.feedback_label.pack(pady=10)

    def check_guess(self):
        try:
            guess = int(self.guess_entry.get())
        except ValueError:
            self.feedback_label.config(text="❌ Invalid input! Enter a number.")
            return

        self.attempts += 1

        if guess < self.secret_number:
            self.feedback_label.config(text="📉 Too low! Try again.", fg="darkred")
            play_sound("wrong.wav")
        elif guess > self.secret_number:
            self.feedback_label.config(text="📈 Too high! Try again.", fg="darkred")
            play_sound("wrong.wav")
        else:
            self.feedback_label.config(text=f"🎉 Correct! You guessed it in {self.attempts} attempts.", fg="green")
            play_sound("win.wav")
            save_score(self.name, self.attempts)
            update_high_score(self.name, self.attempts)
            self.end_game()

    def end_game(self):
        self.guess_entry.pack_forget()
        self.submit_button.pack_forget()

        self.play_again_button.pack(pady=5)
        self.reset_button.pack(pady=5)

        self.show_scoreboard()

    def play_again(self):
        self.secret_number = random.randint(1, self.max_number)
        self.attempts = 0
        self.feedback_label.config(text="")
        self.guess_entry.delete(0, tk.END)
        self.guess_entry.pack(pady=5)
        self.submit_button.pack(pady=5)
        self.play_again_button.pack_forget()
        self.reset_button.pack_forget()
        self.scoreboard_frame.pack_forget()
        play_sound("start.wav")

    def reset_game(self):
        self.play_again_button.pack_forget()
        self.reset_button.pack_forget()
        self.feedback_label.config(text="")
        self.scoreboard_frame.pack_forget()

        self.name_entry.delete(0, tk.END)
        self.name_entry.pack(pady=5)
        self.start_button.pack(pady=15)
        self.guess_label.pack_forget()
        self.guess_entry.pack_forget()
        self.submit_button.pack_forget()

    def show_scoreboard(self):
        name, score = get_high_score()
        high_score_text = f"🥇 High Score: {name} - {score} attempts" if name else "🥇 High Score: None"

        self.high_score_label.config(text=high_score_text)
        self.scoreboard_label.config(text=get_scoreboard())

        self.high_score_label.pack(anchor="w")
        self.scoreboard_label.pack(anchor="w", pady=(10, 0))
        self.scoreboard_frame.pack(pady=15)

# Run GUI
root = tk.Tk()
game = NumberGuessingGame(root)
root.mainloop()
