import speech_recognition as sr
import pyttsx3
from googletrans import Translator

# -----------------------------
# Text-to-Speech
# -----------------------------
def speak(text):
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)
    engine.say(text)
    engine.runAndWait()

# -----------------------------
# Speech-to-Text
# -----------------------------
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Please speak now...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("🔎 Recognizing speech...")
        text = recognizer.recognize_google(audio)
        print(f"✅ You said: {text}")
        return text
    except sr.UnknownValueError:
        print("❌ Could not understand the audio.")
        return ""
    except sr.RequestError:
        print("❌ Speech recognition service error.")
        return ""

# -----------------------------
# Translation
# -----------------------------
def translate_text(text, target_language):
    translator = Translator()
    translation = translator.translate(text, dest=target_language)
    print(f"🌍 Translated text: {translation.text}")
    return translation.text

# -----------------------------
# Language Selection
# -----------------------------
def choose_language():
    print("\n🌐 Choose a target language:")
    print("1. Hindi (hi)")
    print("2. Tamil (ta)")
    print("3. Telugu (te)")
    print("4. Spanish (es)")
    print("5. French (fr)")

    choice = input("Enter number (1–5): ")

    languages = {
        "1": "hi",
        "2": "ta",
        "3": "te",
        "4": "es",
        "5": "fr"
    }

    return languages.get(choice, "es")  # Default Spanish

# -----------------------------
# Main Program
# -----------------------------
def main():
    print("\n=== 🎧 Real-Time Speech Translator ===\n")

    target_language = choose_language()

    original_text = speech_to_text()
    if not original_text:
        return

    translated_text = translate_text(original_text, target_language)

    print("🔊 Speaking translation...")
    speak(translated_text)

    print("\n✅ Translation complete!")

if __name__ == "__main__":
    main()
