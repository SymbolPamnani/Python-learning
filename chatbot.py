#Rule-based chatbot

from datetime import datetime

print("==============================")
print("====== WELCOME TO ALEX =======")
print("==============================")
print("Type 'help' to see what I can do.")
print("Type 'bye' to exit.")
print()

def greets():

    while True:
        user_input = input("You: ").lower().strip()

        # Greetings
        if user_input in ["hello", "hi", "hey", "hey alex"]:
            print("Alex: Hey! How are you?")

        elif user_input in ["good morning", "morning"]:
            print("Alex: Good morning! Hope you're having a great day.")

        elif user_input in ["good evening", "evening"]:
            print("Alex: Good evening! How was your day?")

        # Identity
        elif user_input in ["what is your name", "what's your name", "who are you"]:
            print("Alex: I'm Alex, your rule-based AI chatbot!")

        elif user_input in ["what do you do", "what can you do"]:
            print("Alex: I can respond to predefined questions and have a simple conversation.")

        elif user_input in ["what are you made of", "what is your code made of"]:
            print("Alex: I'm made with Python code, rules, conditions, and a little creativity!")

        # How are you
        elif user_input in ["how are you", "how are you doing", "how do you feel"]:
            print("Alex: I'm doing great! Thanks for asking.")

        # User mood
        elif user_input in ["i am good", "i'm good", "i am fine", "i'm fine"]:
            print("Alex: That's great to hear!")

        elif user_input in ["i am sad", "i'm sad", "i feel sad"]:
            print("Alex: I'm sorry to hear that. I hope things get better soon.")

        elif user_input in ["i am happy", "i'm happy"]:
            print("Alex: That's wonderful! Keep that positive energy going.")

        # Help command
        elif user_input == "help":
            print("Alex: Here are some things you can ask me:")
            print("- Hello / Hi / Hey")
            print("- What is your name?")
            print("- What do you do?")
            print("- How are you?")
            print("- What are you made of?")
            print("- What time is it?")
            print("- What is today's date?")
            print("- Tell me a joke")
            print("- Bye / Goodbye")

        # Time
        elif user_input in ["what time is it", "tell me the time", "current time"]:
            current_time = datetime.now().strftime("%I:%M %p")
            print(f"Alex: The current time is {current_time}.")

        # Date
        elif user_input in ["what is today's date", "what is the date", "today's date"]:
            current_date = datetime.now().strftime("%B %d, %Y")
            print(f"Alex: Today's date is {current_date}.")

        # Joke
        elif user_input in ["tell me a joke", "joke"]:
            print("Alex: Why do programmers prefer dark mode?")
            print("Alex: Because light attracts bugs!")

        # Exit
        elif user_input in ["bye", "goodbye", "exit", "quit"]:
            print("Alex: Goodbye! Have a great day!")
            break

        # Unknown input
        else:
            print("Alex: Hmm... I don't understand that yet.")
            print("Alex: Type 'help' to see what I can respond to.")

greets()