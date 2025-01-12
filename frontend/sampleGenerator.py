from openai import OpenAI
import os

API_KEY = "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"
def questions(text):
    messages = [
        {
            "role": "system",
            "content": (
                "You are an artificial intelligence assistant and you need to generate 10 or more questions based on text given. The text will be from"
                "a random pdf on a subject a student is learning. Make these questions unique and engaging, and make them multiple choice. Print the question"
                "and display 4 or more possible answer choices. highlight the correct one. do not cite any sources in the response"
            ),
        },
        {   
            "role": "user",
            "content": (
                f"here is the text excerpt to generate questions on {text}."
            ),
        },
    ]
    print (API_KEY)
    client = OpenAI(api_key=API_KEY, base_url="https://api.perplexity.ai")

    # chat completion without streaming
    response = client.chat.completions.create(
        model="llama-3.1-sonar-small-128k-online",
        messages=messages
    )
    return response

response = questions("Calculus")
print(response)