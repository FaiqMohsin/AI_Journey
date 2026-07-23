# Day 9 - Modules, pip, Virtual Environments

# PART 1 - Built-in Modules
# Python ships with hundreds of ready-made modules
# you just import and use them — no installation needed
import math        # mathematical functions
import random      # random number generation
import datetime    # working with dates and times
import os          # interacting with your operating system

print("PART 1 - Built-in Modules")
print(f"Pi: {math.pi}")
print(f"Square root of 64: {math.sqrt(64)}")
print(f"Random number: {random.randint(1, 100)}")
print(f"Today: {datetime.date.today()}")
print(f"Current folder: {os.getcwd()}")

# PART 2 - Creating Your Own Module
# any .py file is a module
# you split your code into files and import between them
# this is how every real AI project is structured


# first create helper.py
helper_code = """
def greet(name):
    return f"Hello {name}, welcome to AI engineering!"

def celsius_to_fahrenheit(c):
    return (c * 9/5) + 32

APP_NAME = "AI Journey"
VERSION = "1.0"
"""

with open("helper.py", "w") as f:
    f.write(helper_code)

import helper

print("\nPART 2 - Custom Module")
print(helper.greet("Faiq"))
print(f"37°C in Fahrenheit: {helper.celsius_to_fahrenheit(37)}")
print(f"App: {helper.APP_NAME} v{helper.VERSION}")

# PART 3 - Environment Variables
# storing secrets like API keys safely
# never hardcode keys in your code — use .env files
# this is standard in every professional AI project
import os

# set an environment variable
os.environ["MY_APP_NAME"] = "AI Journey"
os.environ["MY_VERSION"] = "1.0"

# read it back
app_name = os.environ.get("MY_APP_NAME", "Unknown")
version = os.environ.get("MY_VERSION", "0.0")

print("\nPART 3 - Environment Variables")
print(f"App Name: {app_name}")
print(f"Version: {version}")

# PART 4 - Show installed packages
# see everything pip has installed
# this is what requirements.txt captures
import subprocess

print("\nPART 4 - Installed Packages")
result = subprocess.run(["pip", "list"], capture_output=True, text=True)
print(result.stdout[:500])  # print first 500 characters only

# PART 5 - Real world structure
# this is how a real AI project folder looks
# you'll use this structure for every project from now on
import os

folders = ["src", "data", "outputs", "prompts"]
for folder in folders:
    os.makedirs(folder, exist_ok=True)
print("\nPART 5 - Project Structure Created")
print("Your professional project structure:")
for item in os.listdir("."):
    print(f"  {item}")