# Day 3 - File Handling and Error Handling

#write in a file
student = ["John", "Doe", "Jane", "Smith"]
with open("students.txt", "w") as f:
    for student in student:
        f.write(student + "\n")
print(f"Data Written to file successfully.")

#read from a file
with open ("students.txt","r") as f:
    content = f.readlines()
    print ("Students from student file:\n")
    for line in content:
        print(line.strip())

#append in a file 
newstudent = input("Enter the name of the new student: ")
with open ("students.txt","a") as f:
    f.write(f"{newstudent}\n")
print(f"Data appended to file successfully.")

#error Handling
while True:
    try:
        num1 = int(input("Enter a number: "))
        num2 = int(input("Enter another number: "))
        result = num1 / num2
        print(f"The result of {num1} divided by {num2} is {result}.")
        break
    except ValueError:
        print("Invalid input. Please enter a valid number.")
    except ZeroDivisionError:
        print("Error: Division by zero cannot be done enter non zero number.")

#error handling with file
try:
    with open("students.txt", "r") as f:
        content = f.read()
        print(content)
except FileNotFoundError:
    print("Error: The file does not exist.")