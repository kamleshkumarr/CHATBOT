import os
from huggingface_hub import InferenceClient

# -------------------------------
# HuggingFace client
# -------------------------------
token = os.environ.get("HF_TOKEN")
if not token:
    print("WARNING: HF_TOKEN not found in environment!")

client = InferenceClient(api_key=token)

# -------------------------------
# Chatbot with MISTRAL-7B support
# -------------------------------
def get_ai_response(messages):
    global client
    try:
        # Switching to a slightly larger version (7B) which is more consistently 
        # supported on the HuggingFace Chat Completion API.
        completion = client.chat_completion(
            model="Qwen/Qwen2.5-7B-Instruct",
            messages=messages,
            max_tokens=200,
            temperature=0.7,
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"AI Error: {repr(e)}")
        return "I'm having trouble thinking right now. Please try again later."


# -------------------------------
# Sentiment Analysis
# -------------------------------
def get_sentiment(message):
    result = client.text_classification(
        message,
        model="finiteautomata/bertweet-base-sentiment-analysis",
    )

    top = result[0]

    return {
        "label": top["label"],
        "score": round(top["score"], 2)
    }


# -------------------------------
# Summarization
# -------------------------------
def get_summary(message):
    result = client.summarization(
        message,
        model="csebuetnlp/mT5_multilingual_XLSum",
    )

    return result.summary_text