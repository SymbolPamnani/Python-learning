import random

chars= "1234567890!@#$%^&*abdcef"
password=""

for i in range(8):
    password+=random.choice(chars)
    
print("Generated password is: ", password)