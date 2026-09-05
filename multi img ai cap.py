import os
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

# -----------------------------
# Load captioning model
# -----------------------------
def load_caption_model():
    model_name = "Salesforce/blip-image-captioning-base"
    processor = BlipProcessor.from_pretrained(model_name)
    model = BlipForConditionalGeneration.from_pretrained(model_name)
    return processor, model


# -----------------------------
# Generate caption for one image
# -----------------------------
def generate_caption(image_path, processor, model):
    image = Image.open(image_path).convert("RGB")
    inputs = processor(images=image, return_tensors="pt")
    out = model.generate(**inputs, max_new_tokens=30)
    caption = processor.decode(out[0], skip_special_tokens=True)
    return caption


# -----------------------------
# Main multi-image workflow
# -----------------------------
def main():
    print("🧠 Multi-Image AI Captioning Challenge")
    print("Provide image paths, get AI-generated captions, and save a report.\n")
    print("Type 'done' when you are finished adding images.\n")

    processor, model = load_caption_model()
    captions = []  # list of (image_path, caption)

    while True:
        img_path = input("Enter image path (or 'done' to finish): ").strip()

        if img_path.lower() == "done":
            break

        if not os.path.isfile(img_path):
            print("❌ File not found. Try again.\n")
            continue

        try:
            print("✨ Generating caption...")
            caption = generate_caption(img_path, processor, model)
            print(f"📝 Caption: {caption}\n")
            captions.append((img_path, caption))
        except Exception as e:
            print("❌ Error generating caption:", e, "\n")

    if not captions:
        print("No images processed. Exiting.")
        return

    # -----------------------------
    # Save report
    # -----------------------------
    report_name = "captions_report.txt"
    with open(report_name, "w", encoding="utf-8") as f:
        f.write("AI Captioning Report\n")
        f.write("====================\n\n")
        for path, cap in captions:
            f.write(f"Image: {path}\n")
            f.write(f"Caption: {cap}\n")
            f.write("-" * 40 + "\n")

    print(f"\n✅ Report saved as: {report_name}")
    print("Challenge complete! 🎉")


if __name__ == "__main__":
    main()