import os
from PIL import Image
import torch
from diffusers import StableDiffusionInpaintPipeline

# -----------------------------
# Load inpainting model
# -----------------------------
def load_pipeline():
    model_id = "runwayml/stable-diffusion-inpainting"

    pipe = StableDiffusionInpaintPipeline.from_pretrained(
        model_id,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
    )

    device = "cuda" if torch.cuda.is_available() else "cpu"
    pipe = pipe.to(device)

    return pipe, device


# -----------------------------
# Core inpainting function
# -----------------------------
def heal_vintage_photo(pipe, device, image_path, mask_path, prompt):
    # Load images
    original = Image.open(image_path).convert("RGB")
    mask = Image.open(mask_path).convert("L")  # mask as grayscale

    # Optionally resize to 512x512 for best results
    original = original.resize((512, 512))
    mask = mask.resize((512, 512))

    # Run inpainting
    result = pipe(
        prompt=prompt,
        image=original,
        mask_image=mask,
        guidance_scale=7.5,
        num_inference_steps=40,
    )

    healed = result.images[0]
    return healed


# -----------------------------
# Main CLI flow
# -----------------------------
def main():
    print("🧵 Vintage Photo Healer – Stable Diffusion Inpainting")
    print("Restore damaged areas of a vintage photo using a mask + prompt.\n")

    pipe, device = load_pipeline()

    while True:
        image_path = input("Path to vintage photo (or 'exit' to quit): ").strip()
        if image_path.lower() == "exit":
            print("Goodbye.")
            break

        if not os.path.isfile(image_path):
            print("❌ Image file not found. Try again.\n")
            continue

        mask_path = input("Path to mask image (white = repair, black = keep): ").strip()
        if not os.path.isfile(mask_path):
            print("❌ Mask file not found. Try again.\n")
            continue

        prompt = input("Describe how to restore the damaged area:\n> ").strip()
        if not prompt:
            prompt = "restore the damaged area in a realistic vintage photographic style"

        print("\n✨ Healing vintage photo... this may take a moment...\n")

        try:
            healed = heal_vintage_photo(pipe, device, image_path, mask_path, prompt)
            out_file = "healed_vintage.png"
            healed.save(out_file)
            print(f"✅ Saved restored photo as: {out_file}")

            try:
                os.startfile(out_file)  # Windows auto-open
            except:
                print("⚠️ Could not auto-open image. Open 'healed_vintage.png' manually.")
        except Exception as e:
            print("❌ Error during inpainting:", e)

        print("\n---------------------------------\n")


if __name__ == "__main__":
    main()