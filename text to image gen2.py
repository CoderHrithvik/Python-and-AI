from diffusers import StableDiffusionPipeline
import torch
# Load model (downloads once, then offline)

model_id = "runwayml/stable-diffusion-v1-5"
pipe = StableDiffusionPipeline.from_pretrained(
    model_id,
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
)

# Use GPU if available

device = "cuda" if torch.cuda.is_available() else "cpu"
pipe = pipe.to(device)
print("🔥 OFFLINE AI IMAGE GENERATOR READY")
print("Type quit to exit\n")

while True:
    prompt = input("Enter prompt: ")

    if prompt.lower() == "quit":
        break
    print("Generating image...")
    image = pipe(prompt).images[0]
    filename = "offline_image.png"
    image.save(filename)
    print("Saved:", filename)
    image.show()