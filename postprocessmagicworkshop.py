import time
import requests
from PIL import Image, ImageEnhance, ImageFilter
from io import BytesIO
from config import HF_API_KEY
import os

# ---------------------------------------------------------
# MODELS THAT WORK WITH FREE HUGGINGFACE INFERENCE ROUTER
# ---------------------------------------------------------
MODELS = [
    "stabilityai/stable-diffusion-xl-base-1.0",
    "stabilityai/stable-diffusion-2-1",
    "runwayml/stable-diffusion-v1-5",
]

HEADERS = {
    "Authorization": f"Bearer {HF_API_KEY}",
    "Accept": "image/png"
}

# ---------------------------------------------------------
# IMAGE GENERATION
# ---------------------------------------------------------
def generate_image_from_text(prompt):
    """Returns a PIL.Image from text prompt."""
    payload, last_err = {"inputs": prompt}, None

    for model in MODELS:
        print(f"🔍 Trying model: {model}")
        url = f"https://router.huggingface.co/hf-inference/models/{model}"

        for _ in range(3):
            r = requests.post(url, headers=HEADERS, json=payload, timeout=120)
            ct = (r.headers.get("content-type") or "").lower()

            # Successful image response
            if r.status_code == 200 and "application/json" not in ct:
                try:
                    return Image.open(BytesIO(r.content)).convert("RGB")
                except Exception as e:
                    last_err = f"Could not decode image bytes: {e}"
                    break

            # Error response
            try:
                body = r.json() if "application/json" in ct else r.text
            except Exception:
                body = r.text

            last_err = f"Request failed with status code {r.status_code}: {body}"
            break

    raise Exception(last_err or "Unknown error")


# ---------------------------------------------------------
# POST-PROCESSING MODES
# ---------------------------------------------------------
def daylight_edition(image):
    """Brighter, softer look."""
    img = ImageEnhance.Brightness(image).enhance(1.3)
    img = ImageEnhance.Contrast(img).enhance(1.1)
    img = img.filter(ImageFilter.GaussianBlur(radius=1))
    return img


def night_mood(image):
    """Higher contrast, darker, subtle blur."""
    img = ImageEnhance.Brightness(image).enhance(0.8)
    img = ImageEnhance.Contrast(img).enhance(1.4)
    img = img.filter(ImageFilter.GaussianBlur(radius=0.5))
    return img


# ---------------------------------------------------------
# MAIN PROGRAM
# ---------------------------------------------------------
def main():
    print("🎨 Welcome to the Post‑Processing Magic Workshop!")
    print("This program generates an AI image and creates two editions:")
    print("  • Daylight Edition (bright + soft)")
    print("  • Night Mood (contrast + moody)")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("Enter a description for the image:\n> ")

        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        try:
            print("\n✨ Generating base image...")
            base_image = generate_image_from_text(user_input)

            print("🌞 Creating Daylight Edition...")
            day_img = daylight_edition(base_image)

            print("🌙 Creating Night Mood Edition...")
            night_img = night_mood(base_image)

            # Save both versions
            timestamp = int(time.time())
            day_file = f"daylight_{timestamp}.png"
            night_file = f"night_{timestamp}.png"

            day_img.save(day_file)
            night_img.save(night_file)

            print(f"\nSaved:")
            print(f"  • {day_file}")
            print(f"  • {night_file}")

            # Auto-open both images
            try:
                os.startfile(day_file)
                os.startfile(night_file)
            except:
                print("⚠️ Could not auto-open images. Please open them manually.")

            print("\nDone!\n")

        except Exception as e:
            print("\n❌ Error:", e)
            print("Try again.\n")


if __name__ == "__main__":
    main()