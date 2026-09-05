import os
import torch
from diffusers import StableDiffusionPipeline
from datetime import datetime
from PIL import Image

# -----------------------------
# Load Stable Diffusion model
# -----------------------------
model_id = "runwayml/stable-diffusion-v1-5"

pipe = StableDiffusionPipeline.from_pretrained(
    model_id,
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
)

device = "cuda" if torch.cuda.is_available() else "cpu"
pipe = pipe.to(device)

print("🔥 ULTIMATE TEXT‑TO‑IMAGE GENERATOR READY")
print("Type 'quit' to exit.\n")

# -----------------------------
# Style Presets
# -----------------------------
STYLE_PRESETS = {
    "anime": "anime style, vibrant colors, clean line art, highly detailed",
    "pixar": "Pixar 3D style, soft lighting, expressive characters, cinematic",
    "cyberpunk": "cyberpunk neon lights, futuristic, dark city, rain reflections",
    "watercolor": "watercolor painting, soft edges, artistic brush strokes",
    "realistic": "ultra realistic, 8k photography, sharp details, natural lighting",
    "fantasy": "fantasy art, magical atmosphere, epic scenery, mystical lighting",
    "none": ""
}

# -----------------------------
# Automatic Negative Prompt
# -----------------------------
AUTO_NEGATIVE = (
    "blurry, distorted, low quality, extra fingers, bad anatomy, "
    "grainy, low resolution, deformed, mutated, watermark, text"
)

# -----------------------------
# Random Prompt Generator
# -----------------------------
import random

RANDOM_PROMPTS = [
    "a futuristic city floating in the sky",
    "a dragon made of neon light",
    "a peaceful cottage in a magical forest",
    "a robot painting a portrait",
    "a cosmic whale swimming through space",
    "a knight riding a cyberpunk motorcycle",
    "a glowing crystal temple in the mountains"
]

# -----------------------------
# Image-to-Image Mode
# -----------------------------
def load_image(path):
    try:
        return Image.open(path).convert("RGB")
    except:
        print("❌ Could not load image.")
        return None

# -----------------------------
# Main Loop
# -----------------------------
while True:
    print("\n--- MAIN MENU ---")
    print("1. Normal text-to-image")
    print("2. Random prompt")
    print("3. Image-to-image")
    print("Type 'quit' to exit.\n")

    choice = input("Choose option: ").strip().lower()

    if choice == "quit":
        break

    # -----------------------------
    # Prompt Selection
    # -----------------------------
    if choice == "1":
        prompt = input("Enter prompt: ")

    elif choice == "2":
        prompt = random.choice(RANDOM_PROMPTS)
        print("🎲 Random prompt selected:", prompt)

    elif choice == "3":
        img_path = input("Enter path to input image: ")
        init_image = load_image(img_path)
        if init_image is None:
            continue
        prompt = input("Enter prompt for image-to-image: ")

    else:
        print("Invalid choice.")
        continue

    # -----------------------------
    # Style Preset
    # -----------------------------
    print("\nAvailable styles:", ", ".join(STYLE_PRESETS.keys()))
    style = input("Choose style: ").lower()

    if style not in STYLE_PRESETS:
        print("Invalid style. Using none.")
        style = "none"

    styled_prompt = prompt + ", " + STYLE_PRESETS[style]

    # -----------------------------
    # Negative Prompt
    # -----------------------------
    negative_prompt = input("Negative prompt (leave blank for auto): ")

    if negative_prompt.strip() == "":
        negative_prompt = AUTO_NEGATIVE

    # -----------------------------
    # Steps
    # -----------------------------
    try:
        steps = int(input("Inference steps (20–50 recommended): ") or 30)
    except:
        steps = 30

    # -----------------------------
    # Guidance
    # -----------------------------
    try:
        guidance = float(input("Guidance scale (1–15): ") or 7.5)
    except:
        guidance = 7.5

    # -----------------------------
    # Resolution
    # -----------------------------
    resolution = input("Resolution (e.g., 512 or 768x512): ").lower().replace(" ", "")

    try:
        if "x" in resolution:
            w, h = resolution.split("x")
            width = int(w)
            height = int(h)
        else:
            width = int(resolution)
            height = int(resolution)
    except:
        print("Invalid resolution. Using 512x512.")
        width, height = 512, 512

    # -----------------------------
    # Seed
    # -----------------------------
    seed_input = input("Seed (blank = random): ")

    if seed_input.strip() == "":
        generator = torch.Generator(device=device)
    else:
        try:
            generator = torch.Generator(device=device).manual_seed(int(seed_input))
        except:
            generator = torch.Generator(device=device)

    # -----------------------------
    # Batch Generation
    # -----------------------------
    try:
        batch = int(input("How many images to generate? (1–5): ") or 1)
        batch = max(1, min(batch, 5))
    except:
        batch = 1

    print("\n🎨 Generating images...\n")

    # -----------------------------
    # Generate Images
    # -----------------------------
    if choice == "3":
        # Image-to-image mode
        result = pipe(
            prompt=styled_prompt,
            negative_prompt=negative_prompt,
            num_inference_steps=steps,
            guidance_scale=guidance,
            width=width,
            height=height,
            generator=generator,
            image=init_image
        )
        images = result.images
    else:
        # Text-to-image mode
        images = pipe(
            prompt=styled_prompt,
            negative_prompt=negative_prompt,
            num_inference_steps=steps,
            guidance_scale=guidance,
            width=width,
            height=height,
            generator=generator,
            num_images_per_prompt=batch
        ).images

# -----------------------------
# Save image (always same file)
# -----------------------------
filename = "generated_image.png"
image.save(filename)
print("Saved:", filename)

# -----------------------------
# Try multiple ways to open it
# -----------------------------
try:
    os.startfile(filename)  # Windows default viewer
except:
    try:
        Image.open(filename).show()  # PIL fallback
    except:
        print("⚠️ Could not auto-open image. Please open generated_image.png manually.")