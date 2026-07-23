# Day 7 - AI Journal App

import cohere

client = cohere.ClientV2(api_key="cohere_uqewmYGinVgU2UhnWe0jtLLzr0gnFXtgWrpmZR810tRS9u")

print("Welcome!")
 
messages = [
    {"role": "system", "content": "You are a helpful AI Journal assistant corrects any mistakes in user journals and returns a new corrected journal without heighlighting mistakes or giving suggestions"}
]


while True:
    print("\nPlease Enter Your Journal Entry or Kindly Type 'exit' to exit.\n")
    user_input = input("You: ")
    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    messages.append({"role": "user", "content": user_input})

    # send full conversation history to AI
    response = client.chat(
        model="command-a-plus-05-2026",
        messages=messages
    )

    # extract text from response
    reply = ""
    for block in response.message.content:
        if hasattr(block, 'text'):
            reply += block.text

    # add AI reply to memory
    messages.append({"role": "assistant", "content": reply})

    print(f"AI: {reply}\n")

    print ("Would you like to store your write in the journal or upgraded AI Version (AI/Mine)?")
    choice = input()
    if choice.lower() == "ai":
        with open("journal.txt", "a",encoding="utf-8") as f:
            f.write("AI Journal:\n" + reply + "\n\n")
    elif choice.lower() == "mine":
        with open("journal.txt", "a",encoding="utf-8") as f:
            f.write("MyJournal:\n" + user_input + "\n\n")
    print("Your journal entry has been stored in the Journal.\n")