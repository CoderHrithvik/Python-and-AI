import pyaudio
import wave
import threading
import sys
import time
import numpy as np
import matplotlib.pyplot as plt
import speech_recognition as sr
from colorama import Fore, init

init(autoreset=True)

stop_event = threading.Event()

# -----------------------------
# Stop recording when Enter is pressed
# -----------------------------
def wait_for_enter():
    input(Fore.CYAN + "\nPress ENTER to stop recording...\n")
    stop_event.set()

# -----------------------------
# Spinner animation
# -----------------------------
def spinner():
    chars = "|/-\\"
    i = 0
    while not stop_event.is_set():
        sys.stdout.write(Fore.YELLOW + f"\rRecording... {chars[i % 4]}")
        sys.stdout.flush()
        i += 1
        time.sleep(0.1)
    print(Fore.GREEN + "\nRecording stopped.")

# -----------------------------
# Record microphone audio
# -----------------------------
def record_audio():
    p = pyaudio.PyAudio()
    rate = 16000
    chunk = 1024

    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk)

    frames = []

    threading.Thread(target=wait_for_enter, daemon=True).start()
    threading.Thread(target=spinner, daemon=True).start()

    while not stop_event.is_set():
        frames.append(stream.read(chunk))

    stream.stop_stream()
    stream.close()
    width = p.get_sample_size(pyaudio.paInt16)
    p.terminate()

    return b"".join(frames), rate, width

# -----------------------------
# Save WAV file
# -----------------------------
def save_audio(data, rate, width):
    with wave.open("speech.wav", "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(width)
        wf.setframerate(rate)
        wf.writeframes(data)
    print(Fore.GREEN + "Saved audio as speech.wav")

# -----------------------------
# Plot waveform
# -----------------------------
def plot_waveform(data, rate):
    samples = np.frombuffer(data, dtype=np.int16)
    t = np.linspace(0, len(samples) / rate, len(samples))

    plt.figure(figsize=(10, 4))
    plt.plot(t, samples, color="blue")
    plt.title("Speech Waveform")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.grid(True, alpha=0.3)
    plt.show()

# -----------------------------
# Transcribe speech
# -----------------------------
def transcribe(data, rate, width):
    recognizer = sr.Recognizer()
    audio = sr.AudioData(data, rate, width)

    try:
        text = recognizer.recognize_google(audio)
        print(Fore.GREEN + "\nTranscription:")
        print(Fore.WHITE + text)

        with open("speech.txt", "w", encoding="utf-8") as f:
            f.write(text)

        print(Fore.GREEN + "Saved transcription as speech.txt")
    except sr.UnknownValueError:
        print(Fore.RED + "Could not understand the audio.")
    except sr.RequestError:
        print(Fore.RED + "Speech recognition service unavailable.")

# -----------------------------
# Main
# -----------------------------
def main():
    print(Fore.CYAN + "🎤 Voice Recorder & Transcriber")
    print(Fore.CYAN + "--------------------------------")

    audio_data, rate, width = record_audio()
    save_audio(audio_data, rate, width)
    plot_waveform(audio_data, rate)
    transcribe(audio_data, rate, width)

if __name__ == "__main__":
    main()
