from openai import OpenAI

YOUR_API_KEY = "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"
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

    client = OpenAI(api_key=YOUR_API_KEY, base_url="https://api.perplexity.ai")

    # chat completion without streaming
    response = client.chat.completions.create(
        model="llama-3.1-sonar-small-128k-online",
        messages=messages
    )
    return response

with open('sample.txt', 'r', encoding='utf-8') as file:
    text = file.read()
response = questions(text)
print(response)