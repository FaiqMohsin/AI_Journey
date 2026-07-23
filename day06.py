# Day 6 - Cohere Chatbot with Custom Behavior and Memory

import cohere

client = cohere.ClientV2(api_key="your_api_key_here")

# user defines the AI behavior before chatting
print("Welcome! First, define how the AI should behave.")
system_behavior = input("Describe AI behavior (e.g. 'talk like a pirate' or 'explain like I am 10'): ")

# start conversation history with user defined system prompt
messages = [
    {"role": "system", "content": system_behavior}
]
# everything the user and AI say gets added here
# this is the memory - grows every turn

print("\nChatbot ready. Type 'quit' to exit.\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "quit":
        print("Goodbye!")
        break

    # add user message to memory
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