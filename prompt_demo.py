
import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load API keys safely
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

def ask_ai(prompt):
    """Send a prompt to the AI and return the response."""
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def main():
    print("\n=== LIVE PROMPT IMPROVEMENT DEMO ===\n")

    # 1. Vague prompt
    vague_prompt = "Tell me about technology"
    print("🟦 VAGUE PROMPT:")
    print(vague_prompt)
    vague_response = ask_ai(vague_prompt)
    print("\n🟩 AI RESPONSE:")
    print(vague_response)
    print("\n" + "-"*60 + "\n")

    # 2. More specific prompt
    specific_prompt = "Explain how AI works in self-driving cars"
    print("🟦 SPECIFIC PROMPT:")
    print(specific_prompt)
    specific_response = ask_ai(specific_prompt)
    print("\n🟩 AI RESPONSE:")
    print(specific_response)
    print("\n" + "-"*60 + "\n")

    # 3. Context-rich prompt
    context_prompt = (
        "Given the advancements in autonomous vehicles, "
        "explain how AI is used in self-driving cars to make real-time driving decisions."
    )
    print("🟦 CONTEXT-RICH PROMPT:")
    print(context_prompt)
    context_response = ask_ai(context_prompt)
    print("\n🟩 AI RESPONSE:")
    print(context_response)
    print("\n" + "-"*60 + "\n")

    # Reflection questions
    print("=== REFLECTION QUESTIONS ===\n")
    print("1. How did the AI's response change when the prompt was made more specific?")
    print("2. How did the AI's response improve with the added context?")
    print("3. Which prompt produced the most relevant and tailored response? Why?\n")

if __name__ == "__main__":
    main()
