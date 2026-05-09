import re

stop_words = {
    "the", "is", "in", "and", "to",
    "of", "a", "for", "on", "with",
    "as", "by", "an", "at"
}

def clean_text(text):

    text = text.lower()

    text = re.sub(r'[^a-zA-Z ]', '', text)

    words = text.split()

    filtered_words = []

    for word in words:

        if word not in stop_words:

            filtered_words.append(word)

    return " ".join(filtered_words)
