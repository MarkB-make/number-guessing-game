import random
import os

# Get high score from file
def get_high_score():
    if os.path.exists("highscore.txt"):
        with open("highscore.txt", "r") as file:
            line = file.readline().strip()
            if line:
                name, score = line.split(":")
                return name, int(score)
    return None, float('inf')

# Save high score to file
def save_high_score(name, score):
    with open("highscore.txt", "w") as file:
        file.write(f"{name}:{score}")

# Save each player's score to scoreboard
def save_to_scoreboard(name, score):
    with open("scoreboard.txt", "a") as file:
        file.write(f"{name}:{score}\n")

# Display scoreboard leaderboard
def show_leaderboard():
    if not os.path.exists("scoreboard.txt"):
        print("📭 No scores recorded yet!")
        return

    with open("scoreboard.txt", "r") as file:
        entries = []
        for line in file:
            line = line.strip()
            if ':' in line:
                name, score = line.split(":")
                try:
                    entries.append((name, int(score)))
                except ValueError:
                    continue

    if not entries:
        print("📭 No valid scores found.")
        return

    # Sort by attempts (lower is better)
    entries.sort(key=lambda x: x[1])

    print("\n🏆 Top 3 Leaderboard:")
    for i, (name, score) in enumerate(entries[:3], start=1):
        print(f"{i}. {name} - {score} attempts")

# Difficulty settings
def choose_difficulty():
    print("\nChoose difficulty level:")
    print("1. Easy (1-10)")
    print("2. Medium (1-20)")
    print("3. Hard (1-50)")
    while True:
        choice = input("Enter 1, 2, or 3: ")
        if choice == "1":
            return 10
        elif choice == "2":
            return 20
        elif choice == "3":
            return 50
        else:
            print("❌ Invalid choice. Please choose 1, 2, or 3.")

# Main game logic
def play_game():
    player_name = input("🎮 Enter your name: ").strip()
    max_number = choose_difficulty()
    secret_number = random.randint(1, max_number)
    attempts = 0
    guess = None

    print(f"\nI'm thinking of a number between 1 and {max_number}. Can you guess it?")

    while guess != secret_number:
        try:
            guess = int(input("Take a guess: "))
            attempts += 1

            if guess < secret_number:
                print("🔼 Too low!")
            elif guess > secret_number:
                print("🔽 Too high!")
            else:
                print(f"✅ Correct! You guessed it in {attempts} attempts.")
        except ValueError:
            print("❌ Please enter a valid number.")

    # Save results
    save_to_scoreboard(player_name, attempts)
    high_name, high_score = get_high_score()
    if attempts < high_score:
        print(f"🏅 New high score! You beat {high_name or 'None'}'s score of {high_score} attempts.")
        save_high_score(player_name, attempts)
    else:
        print(f"🎯 Current high score is {high_score} by {high_name}.")

# Main menu loop
def main():
    while True:
        print("\n🎲 NUMBER GUESSING GAME")
        print("1. Play Game")
        print("2. View Leaderboard (Top 3)")
        print("3. Exit")

        choice = input("Choose an option (1-3): ")
        if choice == "1":
            play_game()
        elif choice == "2":
            show_leaderboard()
        elif choice == "3":
            print("👋 Goodbye! Thanks for playing.")
            break
        else:
            print("❌ Invalid input. Try again.")

# Run the game
if __name__ == "__main__":
    main()
