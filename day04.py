# Day 4 - Object Oriented Programming

# Part 1 - basic class
class Student:
    def __init__(self, name, age, goal):
        self.name = name
        self.age = age
        self.goal = goal

    def introduce(self):
        print(f"Hi, I am {self.name}, {self.age} years old and my goal is {self.goal}.")

    def study(self, topic):
        print(f"{self.name} is studying {topic}.")

student1 = Student("John", 21, "AI Engineer")
student1.introduce()
student1.study("Python OOP")

# Part 2 - inheritance
class AIStudent(Student):
    def __init__(self, name, age, goal, specialization):
        super().__init__(name, age, goal)
        self.specialization = specialization

    def introduce(self):
        super().introduce()
        print(f"I specialize in {self.specialization}.")

    def build_project(self, project):
        print(f"{self.name} is building {project}.")

ai_student = AIStudent("John", 21, "AI Engineer", "Generative AI")
ai_student.introduce()
ai_student.build_project("AI chatbot")

# Part 3 - real world example
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        print(f"Deposited {amount}. New balance: {self.balance}\n")

    def withdraw(self, amount):
        if amount > self.balance:
            print("Insufficient funds.\n")
        else:
            self.balance -= amount
            print(f"Withdrew {amount}. New balance: {self.balance}\n")

    def show_balance(self):
        print(f"{self.owner}'s balance: {self.balance}\n")

account = BankAccount("John", 1000)
account.show_balance()
account.deposit(500)
account.withdraw(200)
account.withdraw(2000)