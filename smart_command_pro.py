import speech_recognition as sr
import pyttsx3
import random
from datetime import datetime

# ------------------------------------------------------------
# Text‑to‑Speech Engine (initialised once)
# ------------------------------------------------------------
engine = pyttsx3.init()
engine.setProperty("rate", 150)
engine.setProperty("volume", 0.9)

# Default voice index (0 = male, 1 = female on most systems)
current_voice = 0
engine.setProperty("voice", engine.getProperty("voices")[current_voice].id)

# Store user name if they introduce themselves
user_name = None

# ------------------------------------------------------------
# Speak Function
# ------------------------------------------------------------
def speak(text):
    print(f"AI: {text}")
    engine.say(text)
    engine.runAndWait()

# ------------------------------------------------------------
# Listen Function
# ------------------------------------------------------------
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text.lower()
    except sr.UnknownValueError:
        speak("I didn’t catch that. Please try again.")
        return None
    except sr.RequestError:
        speak("Speech service error. Try again later.")
        return None

# ------------------------------------------------------------
# Fun Facts
# ------------------------------------------------------------
FUN_FACTS = [
    "Honey never spoils. Archaeologists found 3000 year old honey that was still good.",
    "Bananas are berries, but strawberries are not.",
    "Octopuses have three hearts.",
    "A day on Venus is longer than a year on Venus.",
    "Some turtles can breathe through their bottoms."
]

# ------------------------------------------------------------
# Main Assistant Logic
# ------------------------------------------------------------
def handle_command(command):
    global user_name, current_voice

    # 1. Date command
    if "date" in command:
        today = datetime.now().strftime("%B %d, %Y")
        speak(f"Today is {today}.")
        return

    # 2. Name introduction
    if command.startswith("my name is"):
        user_name = command.replace("my name is", "").strip().title()
        speak(f"Nice to meet you, {user_name}.")
        return

    # 3. Greeting
    if "hello" in command or "hi" in command:
        if user_name:
            speak(f"Hello {user_name}. How can I help you today.")
        else:
            speak("Hello. What can I do for you.")
        return

    # 4. Fun fact
    if "fact" in command:
        speak(random.choice(FUN_FACTS))
        return

    # 5. Voice switching
    if "use male voice" in command:
        current_voice = 0
        engine.setProperty("voice", engine.getProperty("voices")[0].id)
        speak("Male voice activated.")
        return

    if "use female voice" in command:
        voices = engine.getProperty("voices")
        if len(voices) > 1:
            current_voice = 1
            engine.setProperty("voice", voices[1].id)
            speak("Female voice activated.")
        else:
            speak("Female voice is not available on this system.")
        return

    # 6. Exit
    if "exit" in command or "stop" in command:
        speak("Goodbye.")
        return "exit"

    # 7. Unknown command
    speak("I didn’t understand that. Please try again.")

# ------------------------------------------------------------
# Main Loop
# ------------------------------------------------------------
def main():
    speak("Smart Command Pro activated. Say hello to begin.")

    while True:
        command = listen()
        if command is None:
            continue

        result = handle_command(command)
        if result == "exit":
            break

# ------------------------------------------------------------
if __name__ == "__main__":
    main()
