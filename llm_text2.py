from transformers import pipeline

def build_summarizer(model_name: str):
    # FLAN‑T5 works with the summarization pipeline
    return pipeline("summarization", model=model_name)

def summarize_text(text: str, model_name: str = "google/flan-t5-small",
                   min_len: int = 30, max_len: int = 120):

    summarizer = build_summarizer(model_name)

    result = summarizer(
        text,
        max_length=max_len,
        min_length=min_len,
        do_sample=False
    )

    # FLAN‑T5 returns 'summary_text'
    return result[0]["summary_text"]

def main():
    print("Choose model:")
    print("1. FLAN‑T5 Small (fastest)")
    print("2. FLAN‑T5 Base (better quality)")
    choice = input("Enter 1 or 2: ").strip()

    if choice == "1":
        model = "google/flan-t5-small"
    else:
        model = "google/flan-t5-base"

    min_len = int(input("Min summary length (e.g. 30): ") or 30)
    max_len = int(input("Max summary length (e.g. 120): ") or 120)

    print("\nPaste the text you want to summarize:")
    long_text = input("> ")

    print("\nGenerating summary...\n")

    summary = summarize_text(long_text, model_name=model,
                             min_len=min_len, max_len=max_len)

    print("=== SUMMARY ===")
    print(summary)

if __name__ == "__main__":
    main()