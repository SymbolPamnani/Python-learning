#INVENTORY SYSTEM
inventory = [("Apples", 50), ("Bananas", 75), ("Oranges", 30)]

highh= max(inventory, key=lambda x:x[1])
print("High Quantity: ",highh)

newinv =[]
for item, qty in inventory:
    if item == "Bananas":
        newinv.append((item, qty+20))
print("Quantity added in cart: ", newinv)

inventory.append(("Grape", 60))
print("Updated Inventory: ", inventory)


print("------Inventory------")
print(f"{'Item':<15} {'Quantity':<10}")
for item, qty in inventory:
    print(f"{item:<15} {qty:<10}")