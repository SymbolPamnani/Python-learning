import numpy as np

marks = np.array([
    [90,59,89],
    [76,89,98],
    [90,28,18]
])

#Average marks of each student
avg_student = np.mean(marks, axis=1)
print(f"Average per student: ", avg_student)

#Average per subject
avg_sub = np.mean(marks, axis=0)
print(f"Average per subject: " , avg_sub)

import pandas as pd
df = pd.DataFrame(marks, columns=['English', 'Maths', 'CNDC'])
df['Average'] = df.mean(axis=1)
df['Result'] = np.where(df['Average'] > 60, 'Pass', 'Fail')
print(df)

#Students who have failed
#failed= df[df['Result'] == 'Fail']
#print("Failed students: ", failed)

import matplotlib.pyplot as plt
plt.bar(['Symbol', 'Aakash', 'Kashish'], df['Average'], color= 'green')
plt.title("Average Marks Representation")
plt.ylabel('Marks')
plt.show()

#subject wise average
subjects = ['Maths', 'English', 'CNDC']
plt.bar(subjects, df[subjects].mean(), color='blue')
plt.title("Average Marks Representation")
plt.ylabel('Marks')
plt.show()

#find high score in each subject

print(f"Highest marks in Maths: ", df['Maths'].max)
print(f"Highest marks in English: ", df['English'])
print(f"Highest marks in CNDC: ", df['CNDC'])
#plt.subplot
#students= ['Symbol', 'Aakash', 'Kashish']