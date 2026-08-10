seats = [
    ['O', 'O', 'X', 'O'],  # Row 1: A, B, C, D
    ['X', 'O', 'O', 'X'],  # Row 2
    ['O', 'X', 'O', 'O'],  # Row 3
    ['O', 'O', 'O', 'X'],  # Row 4
    ['X', 'X', 'O', 'O'],  # Row 5
]

for s in seats:
    print(s)

for i, row in enumerate(seats):
    print("Row", i+1, "available seats are", row.count('O'))

seats[1][1] = 'X'
seats[1][2] = 'X'
print("New reserved seats")
for s in seats:
    print(s)

for s in seats:
    print(s[1], s[2])

for s in seats:
    print(s[0], s[3])

gbook ={}
for i, row in enumerate(seats):
    gbook[i+1]= row.count('O')
print("Avail seats: ")
print(gbook)

for i, row in enumerate(seats):
    if row[0] == 'O':   # A seat
        print("Row", i+1, "Seat A")
        break
    elif row[3] == 'O': # D seat
        print("Row", i+1, "Seat D")
        break

total_seats = len(seats) * 4
booked = 0

for s in seats:
    booked += s.count('X')

occupancy = (booked / total_seats) * 100

print("\nOccupancy:", occupancy, "%")