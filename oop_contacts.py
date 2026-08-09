class Contact:

    def __init__(self, name, phone, email):
        self.name = name
        self.phone = phone
        self.email = email

    def show(self):
        print("----------------")
        print("Name :", self.name)
        print("Phone:", self.phone)
        print("Email:", self.email)
        print("----------------")


contacts = []


def dashboard():
    print("======Phone book======")


def welcome():
    print("Press 1 to Add Contact")
    print("Press 2 to Remove Contact")
    print("Press 3 to Show Contact")
    print("Press 4 to Search Contact")
    print("Press 0 to Exit!")


def add_contact():
    name = input("Enter name: ")
    phone = input("Enter phone: ")
    email = input("Enter email: ")

    new_contact = Contact(name, phone, email)
    contacts.append(new_contact)

    print("Contact added successfully")


def show_contact():
    if len(contacts) == 0:
        print("No contact found")
    else:
        for c in contacts:     
            c.show()


def search_contact():
    number = input("Enter the number you want to search: ")

    found = False

    for c in contacts:
        if number == c.phone:
            print("\nContact Found!")
            c.show()
            found = True
            break

    if not found:
        print("Contact not found!")


def remove_contact():
    number = input("Enter the number you want to delete: ")

    found = False

    for c in contacts:
        if number == c.phone:
            c.show()
            contacts.remove(c)
            print("\nContact Removed.")
            found = True
            break

    if not found:
        print("Contact not found!")

choices = [0, 1, 2, 3, 4]


def choose():

    while True:

        dashboard()
        welcome()

        try:
            choice = int(input("Press Any number: "))
        except ValueError:
            print("Please enter a valid number!\n")
            continue

        if choice not in choices:
            print("Invalid choice!\n")
            continue

        if choice == 1:
            add_contact()

        elif choice == 2:
            remove_contact()

        elif choice == 3:
            show_contact()

        elif choice == 4:
            search_contact()

        elif choice == 0:
            print("Thankyou!")
            break
        
choose()