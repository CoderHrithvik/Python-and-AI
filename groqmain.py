from groq import generate_response

def prompt_engineering_activity():
    print("Welcome to the Prompt Engineering Activity!")

    vague = input("Please enter a vague prompt: ")
    print("\nGenerating response for the vague prompt:")
    print(generate_response(vague))

    specific = input("\nNow, please enter a more specific prompt: ")
    print("\nGenerating response for the specific prompt:")
    print(generate_response(specific))

    context = input("\nFinally, please enter your specific prompt with context: ")
    print("\nGenerating response for the contextual prompt:")
    print(generate_response(context))

    print("\n--- Reflection ---")
    print("1. How did the specificity of your prompt affect the quality of the response?")
    print("2. How did the Ai's response improve with the addition of context?")
    print("3. Which prompt gave the most relevant and tailored response? Why do you think that is?")

if __name__ == "__main__":
    prompt_engineering_activity()