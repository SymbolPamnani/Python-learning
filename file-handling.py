# ============================================================
# FILE HANDLING IN PYTHON
# ============================================================

# "r" = Read mode
# Opens the file so we can read its contents.
# You CANNOT use f.write() in read mode.
with open("myfile.txt", "r") as f:
    content = f.read()
    print(content)


# "w" = Write mode
# Creates the file if it does not exist.
# If the file already contains data, "w" will DELETE/REPLACE
# the existing content with whatever we write.
with open("myfile.txt1", "w") as f:
    f.write("May I help you?")


# "a" = Append mode
# Adds new content to the END of the existing file.
# It does not delete the existing content.
with open("myfile.txt2", "a") as f:
    f.write("May I help you?\n")


# ============================================================
# READING A CSV FILE USING PYTHON'S CSV MODULE
# ============================================================

import csv


# Read the CSV file row by row.
# csv.reader() converts each row into a list of values.
with open("salary_dataset.csv", "r") as f:
    read = csv.reader(f)

    for line in read:
        print(line)


# ============================================================
# READING A CSV FILE WHILE SKIPPING THE HEADER
# ============================================================

with open("salary_dataset.csv", "r") as f:
    read = csv.reader(f)

    # Skip the first row (usually the column names/header).
    next(read)

    # Read and print every remaining row.
    for line in read:
        print(line)