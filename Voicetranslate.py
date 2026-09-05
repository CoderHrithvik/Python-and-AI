import speech_recognition as sr
import pyttsx3
from googletrans import Translator
import pyaudio

# ------------------------------------------------------------
# Language Menu
# ------------------------------------------------------------
LANGUAGE_OPTIONS = {
    "1": ("Hindi", "hi"),
    "2": ("Tamil", "ta"),
    "3": ("Telugu", "te"),
    "4": ("Bengali", "bn"),
    "5": ("Marathi", "mr"),
    "6": ("Gujarati", "gu"),
    "7": ("Malayalam", "ml"),
    "8": ("Punjabi", "pa"),
}

# ------------------------------------------------------------
# Text‑to‑Speech
# ------------------------------------------------------------
def speak(text: str, language: str = "en") -> None:
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)
    voices = engine.getProperty("voices")

    # Select voice safely
    if voices:
        if language == "en":
            engine.setProperty("voice", voices[0].id)
        elif len(voices) > 1:
            engine.setProperty("voice", voices[1].id)

    engine.say(text)
    engine.runAndWait()

# ------------------------------------------------------------
# Speech Recognition
# ------------------------------------------------------------
def speech_to_text() -> str:
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("\n🎤 Please speak now in English...")
        recognizer.adjust_for_ambient_noise(source, duration=0.7)
        audio = recognizer.listen(source)

    try:
        print("🔍 Recognizing speech...")
        text = recognizer.recognize_google(audio, language="en-US")
        print(f"✅ You said: {text}")
        return text
    except sr.UnknownValueError:
        print("❌ Could not understand the audio.")
    except sr.RequestError as exc:
        print(f"❌ Speech API Error: {exc}")

    return ""

# ------------------------------------------------------------
# Translation
# ------------------------------------------------------------
def translate_text(text: str, target_language: str) -> str:
    translator = Translator()
    translation = translator.translate(text, dest=target_language)
    print(f"🌍 Translated text: {translation.text}")
    return translation.text

# ------------------------------------------------------------
# Language Selection Menu
# ------------------------------------------------------------
def display_language_options() -> tuple[str, str]:
    print("\n🌍 Available translation languages:")
    for key, (name, code) in LANGUAGE_OPTIONS.items():
        print(f"{key}. {name} ({code})")

    choice = input("Please select the target language number (1–8): ").strip()
    return LANGUAGE_OPTIONS.get(choice, ("Hindi", "hi"))

# ------------------------------------------------------------
# Full Translation Flow
# ------------------------------------------------------------
def run_translator() -> None:
    target_name, target_code = display_language_options()
    print(f"\n➡️ Target language selected: {target_name} ({target_code})")

    original_text = speech_to_text()
    if not original_text:
        print("⚠️ No speech detected. Returning to menu.")
        return

    translated_text = translate_text(original_text, target_code)

    print("🔊 Speaking translated output...")
    speak(translated_text, language="en")
    print("✅ Translation spoken out!")

# ------------------------------------------------------------
# Main Menu Loop
# ------------------------------------------------------------
def main() -> None:
    print("===== AI Voice Translator Console =====")

    while True:
        print("\n1. Start voice translation")
        print("2. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            run_translator()
        elif choice == "2":
            print("👋 Exiting translator. Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")

# ------------------------------------------------------------
if __name__ == "__main__":
    main()
