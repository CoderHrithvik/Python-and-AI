import requests

api_url = "https://github.com/amaiya/ktrain/blob/fdbeda6edfdde0e125d0a258c6c1abd091853da2/FAQ.md?plain=1#L159"

headers = {
"Authorization": "Bearer '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'"
}

text = "I love this movie! It was fantastic."

response = requests.post(api_url, headers=headers, json={"inputs": text})

if response.status_code == 200:
    result = response.json()
    print("Sentiment:", result[0]["label"])
    print("Confidence Score:", result[0]["score"])

else:
    print("Error:", response.status_code)
    print("Message:", response.text) 