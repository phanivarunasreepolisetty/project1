import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

stop_words = set(stopwords.words('english'))
dresses = {
    "jeans": "1000 rupees",
    "lehengas": "2000 rupees",
    "kurthas": "999 rupees",
    "short tops": "800 rupees",
    "long tops": "1000 rupees",
    "tops": "500 rupees",
    "sarees": "1500 rupees",
    "leggings": "600 rupees",
    "chudidhar": "1000 rupees",
    "cloth material": "1200 rupees"
}
def extract_keywords(text):
    return [w for w in word_tokenize(text.lower()) if w.isalnum() and w not in stop_words]

def get_response(text):
    text_lower = text.lower()
    kw = extract_keywords(text)

    if any(g in kw for g in ["hi", "hello", "hey"]):
        return ["Hello! How can I help you?"]

    if any(w in kw for w in ["types", "items", "dresses"]):
        return [f"We offer:\n- " + "\n- ".join(dresses.keys())]

    if any(word in text_lower for word in ["cost", "price", "rate", "charges"]):
        return [f"Prices:\n" + "\n".join(f"- {k.capitalize()}: {v}" for k, v in dresses.items())]

    if text_lower in ["no", "nope", "nah", "not now"]:
        return ["Okay, thanks for interacting! Have a great day! 👋"]

    if "thank" in text_lower:
        return ["You're welcome! 😊"]

    if any(ok in text_lower for ok in ["okay", "ok"]):
        return ["Okay! Need anything else?"]

    if "quit" in text_lower:
        return ["Thank you for visiting. Bye! 👋"]

    match = re.search(r"tell me about (.+)", text_lower)
    if match:
        item = match.group(1).strip(" .!?")
        if item in dresses:
            return [f"{item.capitalize()} costs {dresses[item]}."]
        return [f"Sorry, no info about '{item}'."]

    for dress in dresses:
        if dress in text_lower:
            return [f"{dress.capitalize()} costs {dresses[dress]}."]

    return ["Ask about dress types, prices, or specific items like jeans, lehengas, or tops."]

def chatbot():
    print("👗 Welcome to the Dress Info Bot! Type 'quit' to exit.")
    while True:
        user_input = input("You: ")
        for response in get_response(user_input):
            print(f"Bot: {response}")
        if user_input.lower() in ["quit", "no", "nope", "nah", "not now"]:
            break

if __name__ == "__main__":
    chatbot()
