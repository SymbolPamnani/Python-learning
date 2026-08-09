students = []

def cal_avg(avg):
    if avg >= 95:
        grade = "A++"
    elif avg >= 90:
        grade = "A+"
    elif avg >= 80:
        grade = "B"
    elif avg >= 70:
        grade = "C"
    else:
        grade = "F"

    if grade == "F":
        print("Fail")
    else:
        print("Pass")

    return grade


def add_student():
    
    name = input("Enter name: ")
    rollno = int(input("Enter roll no: "))
    marks = []

    for i in range(3):
        mark = int(input(f"Enter marks for subject {i+1}: "))
        marks.append(mark)

    total = sum(marks)
    average = total / len(marks)
    grade = cal_avg(average)

    student = {
        "Name": name,
        "Reg/no": rollno,
        "Marks": marks,
        "Total": total,
        "Avg": average,
        "Grade": grade
    }

    students.append(student)
    print("Total: ", total)
    print("Average: ", average)
    print("Grade: ", grade)

def display_info():
    if not students:
        print("No Info to Display")
        return

    for student in students:
        print("Name:", student["Name"])
        print("Roll no:", student["Reg/no"])
        print("Marks:", student["Marks"])
       
        print("---------------------")


def highest_marks():
    if not students:
        print("No One to check")
        return
    subjects= len(students[0]["Marks"])
    higher_marks= [0]*subjects
    high_student= [""]*subjects

    for student in students:
        for i in range(subjects):
            if student["Marks"][i] > higher_marks[i]:
                higher_marks[i]=student["Marks"][i]
                high_student[i] = student["Name"]
    print("High Marks in each subject: ")
    for i in range(subjects):
        print(f"Subject {i+1}: {higher_marks[i]} marks by: {high_student[i]}")


def subject_average():
    if not students:
        print("No info present!")
        return
    subjects= len(students[0]["Marks"])
    sub_total=[0] * subjects

    for student in students:
        for i in range(subjects):
            sub_total[i] += student["Marks"][i]

    print("Subject Wise average: ")
    for i in range(subjects):
        avg=sub_total[i] / len(students)
        print(f"Subject {i+1}: {avg:.2f}")

def delete_student():
    if not students:
        print("No info to delete!")
        return
    
    rollno= int(input("Enter Roll no of student you want to delete: "))
    for i in range(len(students)):
        if students[i]["Reg/no"] == rollno:
            remove_student = students.pop(i)
            print(f"Student {remove_student['Name']} with (Reg no: {rollno}) deleted successfully!")
            return

def search_student():
    if not students:
        print("No students!")
        return
    
    search_roll = int(input("Enter roll number to search: "))
    found = False

    for student in students:
        if student["Reg/no"] == search_roll:
            print("Student found!")
            print("Name: ", student["Name"])
            print("Roll no: ", student["Reg/no"])
            print("Marks: ", student["Marks"])
            print("Total: ", student["Total"])
            print("Average: ", student["Avg"])
            print("Grade: ", student["Grade"])
            found= True
            break
    if not found:
            print("Nothing to show")

while True:
    print("1. Add students")
    print("2. Display Students")
    print("3. Display High Marks Student")
    print("4. Search Student")
    print("5. Subject Wise Average")
    print("6. Delete Student")
    print("7. Exit")


    choice = input("Enter choice: ")

    if choice == "1":
        add_student()
    elif choice == "2":
        display_info()
    elif choice == "3":
        highest_marks()
    elif choice == "4":
        search_student()
    elif choice == "5":
        subject_average()
    elif choice== "6":
        delete_student()
    elif choice== "7":
        print("Ended!")
        break
    else:
        print("Invalid input")