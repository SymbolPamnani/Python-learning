import random

choices = ["rock", "paper", "sissors"]

def dashboard():
    print("-------------------------")
    print("------ Rock Paper Sissors Game ------")
    print("-------------------------")


def welcome():
    name = input("Enter your name: ").strip()
    print(f"\nWelcome, {name}!")
    print("Let's play Rock, Paper, Scissors!\n")


def game():

    player_score = 0
    computer_score = 0
    draws = 0

    while True:

        play = input("Do you want to play? (y/n): ").strip().lower()

        if play == "n":
            print("\nThanks for playing!")
            break

        elif play != "y":
            print("Please enter only y or n.\n")
            continue

        print("\nChoose:")
        print("Rock")
        print("Paper")
        print("Scissors")

        choice = input("Your choice: ").strip().lower()

        if choice not in choices:
            print("Invalid choice!\n")
            continue

        computer = random.choice(choices)

        print("\nYou chose:", choice)
        print("Computer chose:", computer)

        if choice == computer:
            print("Result: Draw!")
            draws += 1

        elif (
            (choice == "rock" and computer == "sissors") or
            (choice == "paper" and computer == "rock") or
            (choice == "sissors" and computer == "paper")
        ):
            print("Result: You Win!")
            player_score += 1

        else:
            print("Result: Computer Wins!")
            computer_score += 1

        print("\n------ Scoreboard ------")
        print("Player   :", player_score)
        print("Computer :", computer_score)
        print("Draws    :", draws)
        print("------------------------\n")


dashboard()
welcome()
game()
