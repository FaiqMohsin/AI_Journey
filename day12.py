# Day 12 - Prompt Engineering Techniques

import cohere

client = cohere.ClientV2(api_key="your_cohere_key_here")

def ask(messages, label):
    print(f"\n{'='*50}")
    print(f"TECHNIQUE: {label}")
    print(f"{'='*50}")
    response = client.chat(
        model="command-a-plus-05-2026",
        messages=messages
    )
    for block in response.message.content:
        if hasattr(block, 'text'):
            print(block.text)

# ─────────────────────────────────────────
# TECHNIQUE 1 - Zero Shot
# just ask directly with no examples
# works for simple tasks
# ─────────────────────────────────────────
ask([
    {"role": "user", "content": "Classify this review as positive or negative: 'The food was amazing but service was slow.'"}
], "Zero Shot")

# ─────────────────────────────────────────
# TECHNIQUE 2 - Few Shot
# give examples before your actual question
# dramatically improves accuracy on complex tasks
# ─────────────────────────────────────────
ask([
    {"role": "user", "content": """Classify these reviews as positive or negative:

Review: "Amazing product, love it!" → Positive
Review: "Waste of money, broke in 2 days" → Negative
Review: "Decent quality, nothing special" → Neutral

Now classify this:
Review: "The food was amazing but service was slow."
"""}
], "Few Shot")

# ─────────────────────────────────────────
# TECHNIQUE 3 - Chain of Thought
# tell AI to think step by step
# massively improves accuracy on reasoning tasks
# ─────────────────────────────────────────
ask([
    {"role": "user", "content": """Think step by step and solve this:

A shop buys a shirt for PKR 500. 
They want to make 30% profit.
They also add 10% sales tax on the selling price.
What is the final price the customer pays?

Show your working step by step."""}
], "Chain of Thought")

# ─────────────────────────────────────────
# TECHNIQUE 4 - Role Prompting
# assign AI a specific role
# changes tone, depth, and style of response
# ─────────────────────────────────────────
ask([
    {"role": "system", "content": "You are a senior AI engineer with 10 years of experience. You give direct, technical answers with no fluff."},
    {"role": "user", "content": "Should I learn LangChain or build directly with LLM APIs?"}
], "Role Prompting")

# ─────────────────────────────────────────
# TECHNIQUE 5 - Output Formatting
# tell AI exactly what format you want
# critical when building apps that parse AI output
# ─────────────────────────────────────────
ask([
    {"role": "system", "content": "You always respond in valid JSON only. No explanation. No markdown. Just raw JSON."},
    {"role": "user", "content": "Give me details for a Pakistani student named Faiq who wants to become an AI engineer. Include name, city, goal, skills as a list, and timeline in months."}
], "Output Formatting - JSON")

# ─────────────────────────────────────────
# TECHNIQUE 6 - Prompt Chaining
# break complex tasks into smaller prompts
# feed output of one prompt as input to next
# this is the foundation of LangChain's concept
# ─────────────────────────────────────────
print(f"\n{'='*50}")
print("TECHNIQUE: Prompt Chaining")
print(f"{'='*50}")

# Step 1 - generate a business idea
response1 = client.chat(
    model="command-a-plus-05-2026",
    messages=[
        {"role": "system", "content": "Give exactly one AI startup idea for Pakistan in one sentence only."},
        {"role": "user", "content": "Give me an AI startup idea for Pakistan"}
    ]
)
idea = ""
for block in response1.message.content:
    if hasattr(block, 'text'):
        idea += block.text

print(f"Step 1 - Idea: {idea}")

# Step 2 - use that idea as input to next prompt
response2 = client.chat(
    model="command-a-plus-05-2026",
    messages=[
        {"role": "system", "content": "You are a business analyst. Be concise."},
        {"role": "user", "content": f"For this startup idea: '{idea}'\n\nGive me 3 target customers and 3 revenue streams. Use bullet points."}
    ]
)
print(f"\nStep 2 - Business Analysis:")
for block in response2.message.content:
    if hasattr(block, 'text'):
        print(block.text)