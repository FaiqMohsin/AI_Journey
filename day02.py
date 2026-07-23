# Day 2 - Loops, Lists, Dictionaries

# Part 1 - for loop with list
scores = [85, 92, 78, 90, 88]
total = 0
for score in scores:
    total += score
average = total / len(scores)
print(f"Average score: {average:.2f}")

# Part 2 - while loop
attempts = 3
secret = "python"
while attempts > 0:
    guess = input("Guess the secret word: ")
    if guess == secret:
        print("Correct! You win.")
        break
    attempts -= 1
    print(f"Wrong. {attempts} attempts left.")
if attempts == 0:
    print("You lost. The word was 'python'.")

# Part 3 - dictionary
student = {
    "name": "Joseph",
    "age": 45,
    "city": "Sydney",
    "goal": "AI Engineer"
}
for key, value in student.items():
    print(f"{key}: {value}")

# Part 4 - combine list and dictionary
students = [
    {"name": "Ali", "score": 85},
    {"name": "Sara", "score": 92},
    {"name": "Faiq", "score": 98}
]
for s in students:
    if s["score"] >= 90:
        print(f"{s['name']} got an A with {s['score']}")
    else:
        print(f"{s['name']} got a B with {s['score']}")