seats = [ 
('O', 'O', 'X', 'O'), 
('X', 'O', 'O', 'X'), 
('O', 'X', 'O', 'O') 
] 

for s in seats:
    print(s)

for i,r in enumerate(seats):
   print("In", i+1, "row", r.count('O'), 'seats available')

seats[1][1]

for s in seats:
    s1= s[0], s[3]
    print(s1)

for s in seats:
    s1= s[1], s[2]
    print(s1)

