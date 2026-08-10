products = [ 
{"id": 101, "name": "Laptop", "price": 99.90, "stock": 9, "category": "Electronics"}, 
{"id": 102, "name": "Mouse", "price": 25.50, "stock": 50, "category": "Machenical"}, 
{"id": 103, "name": "Headphones", "price": 15.20, "stock": 20, "category": "Electronics"}, 
{"id": 104, "name": "Mic", "price": 27.00, "stock": 5, "category": "Musical"}, 
{"id": 105, "name": "Speaker", "price": 45.70, "stock": 15, "category": "Electronics"}
] 

print(products)

print(f"{'ID':<5} {'Name':<15} {'Price':<10} {'Stock':<10} {'Category':<5} ")
for p in products:
    print(f"{p['id']:<5} {p['name']:<15} {p['price']:<10} {p['stock']:<10} {p['category']:<5} ")


for p in products:
    if p["stock"] < 10:
        print(p["name"], " need restock")
    else:
        print(p["name"], " is okay")

total = sum(p['price'] * p['stock']for p in products)
print(f"{total}")

for p in products:
    if p["category"] == "Electronics":
        p["price"] = p['price'] * 0.9
    print(p["name"], p["category"],p["price"])

cheap= min(products, key=lambda x:x["price"])
exp= max(products, key=lambda x:x["price"])
protuple= (cheap['name'], exp['name'])
print("Cheap and expensive products: ", protuple)

l1 = [p["name"] for p in products]
print(l1)

councat ={}
for p in products:
    councat[p["category"]] = councat.get(p["category"],0) +1
print(councat)

stockk= [p for p in products if 50<= p['price'] <= 200]
for p in stockk:
    print(f"{p['name']}: {p['price']:.2f}")