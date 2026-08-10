# Student Grade Analyzer - Advanced
import statistics

students = [
    {"name": "Alice", "grades": [85, 90, 78, 92, 88], "attendance": 95},
    {"name": "Bob", "grades": [72, 68, 75, 80, 70], "attendance": 82},
    {"name": "Charlie", "grades": [93, 89, 95, 91, 94], "attendance": 98},
    {"name": "Diana", "grades": [68, 72, 70, 75, 73], "attendance": 78},
    {"name": "Eve", "grades": [88, 85, 90, 87, 92], "attendance": 91},
    {"name": "Frank", "grades": [55, 60, 58, 62, 65], "attendance": 70},
    {"name": "Grace", "grades": [95, 92, 94, 96, 93], "attendance": 96},
    {"name": "Henry", "grades": [82, 79, 84, 81, 85], "attendance": 85},
    {"name": "Ivy", "grades": [70, 75, 72, 78, 74], "attendance": 79},
    {"name": "Jack", "grades": [91, 88, 93, 89, 90], "attendance": 88},
]

# Calculate each student's average
student_averages = []
for student in students:
    avg = sum(student['grades']) / len(student['grades'])
    student['average'] = avg
    student_averages.append({"name": student['name'], "average": avg})

print("Student Averages:")
for s in student_averages:
    print(f"  {s['name']}: {s['average']:.2f}")

# Find students with average > 80 AND attendance > 90
high_performers = [s for s in students if s['average'] > 80 and s['attendance'] > 90]
print(f"\nHigh performers (avg > 80, attendance > 90):")
for s in high_performers:
    print(f"  {s['name']}: avg={s['average']:.2f}, attendance={s['attendance']}%")

# Apply curve: add 5 points to all grades
for student in students:
    student['grades'] = [g + 5 for g in student['grades']]
print("\nAfter applying curve (added 5 points):")
for student in students[:3]:  # Show first 3 as example
    print(f"  {student['name']}'s grades: {student['grades']}")

# Extract first 3 grades of each student
for student in students:
    first_three = student['grades'][:3]
    print(f"\n{student['name']}'s first 3 grades: {first_three}")

# Find students with improving grades (later grades > earlier grades)
improving_students = []
for student in students:
    if all(student['grades'][i] < student['grades'][i+1] for i in range(len(student['grades'])-1)):
        improving_students.append(student['name'])
print(f"\nStudents with improving grades: {improving_students if improving_students else 'None'}")

# Create dictionary of grade ranges to student names
grade_ranges = {
    "90-100": [],
    "80-89": [],
    "70-79": [],
    "60-69": [],
    "Below 60": []
}

for student in students:
    if student['average'] >= 90:
        grade_ranges["90-100"].append(student['name'])
    elif student['average'] >= 80:
        grade_ranges["80-89"].append(student['name'])
    elif student['average'] >= 70:
        grade_ranges["70-79"].append(student['name'])
    elif student['average'] >= 60:
        grade_ranges["60-69"].append(student['name'])
    else:
        grade_ranges["Below 60"].append(student['name'])

print("\nGrade distribution:")
for range_name, students_list in grade_ranges.items():
    if students_list:
        print(f"  {range_name}: {', '.join(students_list)}")

# Calculate class statistics
averages = [s['average'] for s in students]
mean_avg = statistics.mean(averages)
median_avg = statistics.median(averages)
mode_avg = statistics.mode([round(avg) for avg in averages])  # Round for mode

print(f"\nClass Statistics:")
print(f"  Mean average: {mean_avg:.2f}")
print(f"  Median average: {median_avg:.2f}")
print(f"  Mode of averages: {mode_avg}")

# Identify students needing intervention (avg < 60 OR attendance < 75)
intervention_needed = [s for s in students if s['average'] < 60 or s['attendance'] < 75]
print(f"\nStudents needing intervention:")
for s in intervention_needed:
    issues = []
    if s['average'] < 60:
        issues.append(f"low average ({s['average']:.2f})")
    if s['attendance'] < 75:
        issues.append(f"low attendance ({s['attendance']}%)")
    print(f"  {s['name']}: {', '.join(issues)}")