# Day 10 - NumPy

import numpy as np

#Array Operations
# This is why NumPy exists - math on entire arrays at once

print("\nArray Operations")

scores = np.array([85, 92, 78, 90, 88, 76, 95, 83])

print(f"Scores: {scores}")
print(f"Mean: {np.mean(scores)}")
print(f"Max: {np.max(scores)}")
print(f"Min: {np.min(scores)}")
print(f"Sum: {np.sum(scores)}")
print(f"Standard deviation: {np.std(scores):.2f}")
print(f"Scores above 85: {scores[scores > 85]}")
print(f"Add 5 bonus to all: {scores + 5}")


# 2D Arrays (Matrices)
# AI works with 2D data constantly - tables, images, datasets
print("\n2D Arrays")

matrix = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])

print(f"Matrix:\n{matrix}")
print(f"Shape: {matrix.shape}")
print(f"First row: {matrix[0]}")
print(f"First column: {matrix[:, 0]}")
print(f"Element at row 1 col 2: {matrix[1, 2]}")
print(f"Transpose:\n{matrix.T}")


# Real World Example
print("\nReal World Example")
# simulate 5 students, 3 exam scores each
np.random.seed(42)
exam_data = np.random.randint(50, 100, size=(5, 3))
students = ["Faiq", "Ali", "Sara", "Ahmed", "Zara"]

print("Exam scores (3 exams):")
print(exam_data)

averages = np.mean(exam_data, axis=1)
print(f"\nStudent averages:")
for name, avg in zip(students, averages):
    print(f"  {name}: {avg:.1f}")

print(f"\nClass average per exam: {np.mean(exam_data, axis=0)}")
print(f"Highest scorer overall: {students[np.argmax(averages)]}")