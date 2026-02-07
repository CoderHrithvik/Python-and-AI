with open("fer2013.csv", "rb") as f:
    chunk = f.read(200)
    print(chunk)