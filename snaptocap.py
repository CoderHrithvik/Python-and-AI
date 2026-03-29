from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from PIL import Image
from colorama import Fore, init
import torch

init(autoreset=True)

# ---------------------- Device ----------------------
device = "cuda" if torch.cuda.is_available() else "cpu"
print(Fore.YELLOW + f"Using device: {device}")

# ---------------------- Load ViT-GPT2 Captioning ----------------------
print(Fore.YELLOW + "Loading nlpconnect/vit-gpt2-image-captioning (cached locally)...")

caption_model = VisionEncoderDecoderModel.from_pretrained(
    "nlpconnect/vit-gpt2-image-captioning"
).to(device)

caption_processor = ViTImageProcessor.from_pretrained(
    "nlpconnect/vit-gpt2-image-captioning"
)

caption_tokenizer = AutoTokenizer.from_pretrained(
    "nlpconnect/vit-gpt2-image-captioning"
)

# ---------------------- Load GPT-2 Expansion ----------------------
print(Fore.YELLOW + "Loading GPT-2 (cached locally)...")

gpt2_model = GPT2LMHeadModel.from_pretrained("gpt2").to(device)
gpt2_tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

# ---------------------- Caption Image ----------------------
def caption_image(path: str):
    try:
        image = Image.open(path).convert("RGB")

        pixel_values = caption_processor(images=image, return_tensors="pt").pixel_values.to(device)

        with torch.no_grad():
            output_ids = caption_model.generate(
                pixel_values,
                max_length=30,
                num_beams=4
            )

        caption = caption_tokenizer.decode(output_ids[0], skip_special_tokens=True)
        return caption.strip()

    except Exception as e:
        print(Fore.RED + f"[ERROR] Captioning failed: {e}")
        return None

# ---------------------- Expand Caption ----------------------
def expand_caption(caption: str):
    try:
        prompt = f"Expand this into a detailed 30-word description:\n{caption}\n"

        inputs = gpt2_tokenizer(prompt, return_tensors="pt").to(device)

        with torch.no_grad():
            outputs = gpt2_model.generate(
                **inputs,
                max_new_tokens=40,
                temperature=0.8,
                do_sample=True,
                pad_token_id=gpt2_tokenizer.eos_token_id
            )

        text = gpt2_tokenizer.decode(outputs[0], skip_special_tokens=True)
        return text

    except Exception as e:
        print(Fore.RED + f"[ERROR] Expansion failed: {e}")
        return None

# ---------------------- Main ----------------------
def main():
    print(Fore.CYAN + "Snap-to-Caption AI — Local ViT-GPT2 Version")

    image_path = input("Enter image path (e.g., tiger.jpg): ").strip()

    print(Fore.YELLOW + "Generating caption locally...")
    caption = caption_image(image_path)
    if not caption:
        return

    print(Fore.GREEN + f"\nCaption:\n{caption}")

    choice = input("\nExpand to ~30-word description? (y/n): ").lower().strip()
    if choice != "y":
        print(Fore.CYAN + "Done.")
        return

    print(Fore.YELLOW + "Expanding with GPT-2...")
    expanded = expand_caption(caption)
    if not expanded:
        return

    print(Fore.GREEN + "\nExpanded Description:")
    print(expanded)

    print(Fore.CYAN + "\nDone.")

if __name__ == "__main__":
    main()