# Day 5 - Modules, pip, and APIs

# Part 1 - built-in modules
import random
import math
import datetime

print(f"Random number: {random.randint(1, 100)}")
print(f"Square root of 144: {math.sqrt(144)}")
print(f"Today's date: {datetime.date.today()}")

# Part 2 - requests module (external)
import requests

# Free API - no key needed
response = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json")

if response.status_code == 200:
    data = response.json()
    price = data["bpi"]["USD"]["rate"]
    print(f"Current Bitcoin price in USD: ${price}")
else:
    print("Failed to fetch data.")

# Part 3 - sending data with POST
import json

test_data = {
    "name": "Faiq",
    "goal": "AI Engineer",
    "days_completed": 5
}
print(f"\nMy progress data:")
for key, value in test_data.items():
    print(f"{key}: {value}")

# Part 5 - saving API response to file
with open("bitcoin_price.txt", "w") as f:
    f.write(f"Bitcoin price fetched on {datetime.date.today()}\n")
    f.write(f"Price: ${price}\n")
print("\nPrice saved to bitcoin_price.txt")