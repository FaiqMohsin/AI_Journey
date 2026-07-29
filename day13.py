

# Day 13 - LangChain Basics

from langchain_cohere import ChatCohere
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate

# SETUP
llm = ChatCohere(
    cohere_api_key="",
    model="command-a-plus-05-2026"
)

def get_text(response):
    if isinstance(response.content, list):
        for block in response.content:
            if isinstance(block, dict) and block.get('type') == 'text':
                return block['text']
    return response.content

# Prompt Template + Chain
# user defines the topic, template fills it in
# chain pipes template output directly into llm

template = ChatPromptTemplate.from_messages([
    ("system", "You are an expert AI assistant. Be concise and clear."),
    ("human", "Explain {topic} in simple terms.")
])

chain = template | llm

print("LangChain Assistant - type 'quit' to exit\n")

while True:
    topic = input("Enter a topic to learn about: ")
    
    if topic.lower() == "quit":
        print("Goodbye!")
        break
    
    result = chain.invoke({"topic": topic})
    print(f"\nAI: {get_text(result)}\n")
       
