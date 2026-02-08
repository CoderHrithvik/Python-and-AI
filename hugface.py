import requests
from config import HF_API_KEY

MODEL_ID = "facebook/bart-large-mnil"
API_URL = f"https://router.huggingface.co/hf-inference/models/{MODEL_ID}"
HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"} 
TOPICS = ["Sports", "Politics", "Technology", "Health", "Business"]

def ask_hf(headline: str):
    payload = {
        "inputs": headline,
        "parameters": {"candidates_labels": TOPICS}}
    r = requests.post(API_URL, headers=HEADERS, json=payload, timeout=30)

    if not r.ok:
        raise RuntimeError(f"HF error {r.status_code}: {r.text}")
    
    return r.json()

def best_topic(preds: list):
    best = max(preds, key=lambda x: x['score'])
    return best['label'], best['score']

def bar(score: float) -> str:
    pct = score * 100
    blocks = int(pct // 10)
    return "█" * blocks + "░" * (10 - blocks)

def show(headline: str, preds: list):
    top_label, top_score = best_topic(preds)    
    print("\n" 