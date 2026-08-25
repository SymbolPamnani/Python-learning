account= {
    "Name": "Symbol",
    "Pin" : 4321,
    "Balance" : 60000,
    "Type" : "BussinessAccount"
}

print("\n====Mini ATM====")
pin= int(input("Enter your pin: "))

if pin == account["Pin"]:
    while True:
        print("\n1. Check Balance")
        print("2. Deposite Money")
        print("3. Withdraw Money")
        print("4. Account Details")
        print("5. Exit")
        choice= int(input("Press any number of your choice: "))

        if choice == 1:
            print("Your Current balance is: ", account["Balance"])

        elif choice == 2:
            ammount = int(input("Enter the ammount you want to deposite: "))

            if ammount>0:
                account["Balance"] = account["Balance"]+ammount
                print("Deposite succesfully!")
                print("\nYour current balance is: ", account["Balance"])
            else:
                print("Invalid ammount!")

        elif choice == 3:
            amount = int(input("Enter the ammount you want to withdraw: "))

            if amount<=0:
                print("Invalid ammount!")
            elif amount>account["Balance"]:
                print("Insufficient balance!")
            else:
                account["Balance"]=account["Balance"]-amount
                print("Withdraw succesfully!")
                print("\nYour current balance is: ", account["Balance"])  

        elif choice == 4:
            print("Name: ", account["Name"])
            print("Balance: ", account["Balance"])
            print("Type: ", account["Type"])

        elif choice == 5:
            print("Thankyou!")
            break

        else:
            print("Invalid choice!")

else:
    print("Wrong Pin!")