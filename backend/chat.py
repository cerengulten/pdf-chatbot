import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
# Make sure your .env file now has GROQ_API_KEY instead of ANTHROPIC_API_KEY
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask_groq(question: str, context_chunks: list[str], history: list = []) -> str:
    context = "\n\n---\n\n".join(context_chunks)

    # 1. Groq takes the system prompt inside the messages list
    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful assistant that answers questions strictly based on "
                "the provided document context. If the answer is not in the context, "
                "say so honestly — do not make things up."
            )
        }
    ]

    # 2. Build message history
    # (Assuming your history items are objects. If they are dictionaries, use m["role"] and m["content"])
    for m in history:
        messages.append({"role": m.role, "content": m.content})

    # 3. Append current question with context
    messages.append({
        "role": "user",
        "content": f"Context from the document:\n\n{context}\n\nQuestion: {question}"
    })

    # 4. Create the completion using a Groq model
    chat_completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile", # Or use "llama3-8b-8192" for a smaller/faster model
        messages=messages,
        max_tokens=1024
    )
    
    # 5. Return the extracted text
    return chat_completion.choices[0].message.content