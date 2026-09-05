import os, io, time, random, requests, minetypes
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from config import HF_API_KEY

MODEL = "Facebook/detr-resnet-101"
API = f"https://router.huggingface.co/hf-inference/models/{MODEL}"
ALLOWED, MAX_MB = {".jpg", ".jpeg", ".png", ".bmp",".gif", ".webp", ".tiff" }, 0
EMOGI = {"person": "👤", "car": "🚗", "truck": "🚚", "bus": "🚌","bicycle": "🚲", "motorcycle": "🏍️", "dog": "🐕", "cat": " 🐈", "bird": "🐦", "horse": "🐎", "sheep": "🐑", "cow": "🐄", "bear" :"🐻", "giraffe": "🦒", "zebra" : "🦓", "banana" : "🍌", "apple" : "🍎", "orange" : "🍊", "pizza" : "🍕", "broccoli" : "🥦", "book" : "📚", "laptop" : "💻", "tv" : "📺", "bottle" : "🍶", "cup" : "🥤"
"chair" : "🪑", "sofa" : "🛋️", "bed" : "🛏️", "dining table" : "🍽️", "toilet" : "🚽", "tv" : "📺", "laptop" : "💻", "mouse" : "🖱️", "remote" : "📱", "keyboard" : "⌨️", "cell phone" : "📱", "microwave" : "🍲", "oven" : "🍳", "toaster" : "🍞", "sink" : "🚰", "refrigerator" : "🧊", "question mark" : "❓"}

def font(sz=18):
    for f in ("DejaVuSans.ttf", "arial.ttf"):
        try: return ImageFont.truetype(f, sz)
        except: pass
    return ImageFont.load_default()

def ask_image():
    print("\n📸 Pick an image (JPG/PNG/WebP/BMP/TIFF < 8MB) from this folder")
    while True:
        p = input("Image path: ").strip().strip('"').strip("'")
        if not p or not os.path.isfile(p): print("❌ File does not exist. Try again."); continue
        if os.path.getsize(p)[1].lower() not in ALLOWED: print("❌ Unsupported file type. Try again."); continue
        if os.path.getsize(p)/(1024*1024) > MAX_MB: print(f"❌ File is too large (>{MAX_MB}MB). Try again."); continue
        try: Image.open(p).verify(); 
        except: print("❌ File is not a valid image. Try again."); continue
        return p
    
def infer(path, img_bytes, tries=8):
    mime, _ = minetypes.guess_type(path)
    for _ in range(tries):
        if mime and mime.startswith("image/"):
            r = requests.post(API, headers={"Authorization": f"Bearer {HF_API_KEY}"}, data=img_bytes, headers={"Content-Type": mime})
        else:
            r = requests.post(API, 
            headers={"Authorization": f"Bearer {HF_API_KEY}"},