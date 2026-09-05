import configgroq
from huggingface_hub import InferenceClient

MODELS = getattr(
    configgroq,
    "HF_MODELS",
    ["meta-llama/Llama-3.1-8B-Instruct"],
)

def generate_response(prompt: str, temperature: float = 0.3, max_tokens: int = 512) -> str:
    key = getattr(configgroq, "HF_API_KEY", None)
    if not key:
        return "Error: HF_API_KEY missing in configgroq.py"
    
    last_err = None
    for m in MODELS:
        try:
            c = InferenceClient(model=m,token=key)
            r = c.chat_completions(
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens
            )
            return r.choices[0].message.content
        except Exception as e:
            last_err = e

    return (
        "Hugging Face models failed.\n"
        f"Tried models: {MODELS}\n"
        "Fix:\n"
        "1) Switch to groq by importing groq.py in main.py OR\n"
        "2) Replace Hugging Face models in hf.py (HF_MODELS).\n"
        f"Details: {type(last_err).__name__}: {last_err}"
    )