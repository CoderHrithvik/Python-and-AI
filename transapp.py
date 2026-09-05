import speech_recognition as sr
import pyttsx3
from googletrans import Translator

# -----------------------------
# Text-to-Speech
# -----------------------------
def speak(text, language="en"):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)

    voices = engine.getProperty('voices')

    # Try selecting a voice based on language
    selected_voice = None
    for voice in voices:
        if language.lower() in voice.id.lower():
            selected_voice = voice.id
            break

    # Fallback voice
    engine.setProperty('voice', selected_voice if selected_voice else voices[0].id)

    engine.say(text)
    engine.runAndWait()


# -----------------------------
# Speech-to-Text with improved error handling
# -----------------------------
def speech_to_text(language="en-US"):
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("🎤 Listening... Please speak now.")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)

    try:
        print("🔎 Recognizing speech...")
        text = recognizer.recognize_google(audio, language=language)
        print(f"✅ You said: {text}")
        return text

    except sr.UnknownValueError:
        print("❌ I couldn't understand what you said. Try speaking clearly.")
        return ""

    except sr.RequestError:
        print("❌ Network or API error. Check your internet connection.")
        return ""


# -----------------------------
# Translation
# -----------------------------
def translate_text(text, src_language, target_language):
    translator = Translator()
    translation = translator.translate(text, src=src_language, dest=target_language)
    print(f"🌍 Translated text: {translation.text}")
    return translation.text


# -----------------------------
# Language Selection Menu
# -----------------------------
def select_language(prompt):
    languages = {
        "1": ("English", "en"),
        "2": ("Hindi", "hi"),
        "3": ("Tamil", "ta"),
        "4": ("Telugu", "te"),
        "5": ("Spanish", "es"),
        "6": ("French", "fr"),
        "7": ("German", "de"),
        "8": ("Chinese", "zh-cn")
    }

    print(prompt)
    for key, (name, code) in languages.items():
        print(f"{key}. {name} ({code})")

    choice = input("Select option (1-8): ")
    return languages.get(choice, ("English", "en"))


# -----------------------------
# Main Application
# -----------------------------
def main():
    print("=== 🌐 Real-Time Multi-Language Speech Translator ===")

    # Select source language
    src_name, src_code = select_language("\n🎙 Select the SOURCE language:")
    print(f"➡ Source language set to: {src_name}")

    # Select target language
    tgt_name, tgt_code = select_language("\n🔁 Select the TARGET language:")
    print(f"➡ Target language set to: {tgt_name}")

    # Convert source language code to Google speech format
    speech_lang_code = src_code + "-IN" if src_code in ["hi", "ta", "te"] else src_code

    # Speech-to-text
    original_text = speech_to_text(language=speech_lang_code)

    if original_text:
        # Translate
        translated_text = translate_text(original_text, src_language=src_code, target_language=tgt_code)

        # Speak translated text
        speak(translated_text, language=tgt_code)
        print("🔊 Translation spoken out loud!")


if __name__ == "__main__":
    main()
