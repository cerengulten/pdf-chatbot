import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Initialize the Groq client
# Make sure your .env file has: GROQ_API_KEY=your_key_here
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask_groq(question: str, context_chunks: list[str]) -> str:
    # 1. Prepare the context block
    context = "\n\n---\n\n".join(context_chunks)
    
    # 2. Make the call to Groq
    # We use 'llama3-8b-8192' because it's fast and free
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant that answers questions strictly based on "
                    "the provided document context. If the answer is not in the context, "
                    "say so honestly — do not make things up."
                ),
            },
            {
                "role": "user",
                "content": f"Context from the document:\n\n{context}\n\nQuestion: {question}",
            }
        ],
        model="llama-3.1-8b-instant",
        temperature=0.2, # Lower temperature makes the AI more factual/less creative
    )
    
    return chat_completion.choices[0].message.content