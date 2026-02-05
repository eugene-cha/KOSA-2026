import os
from openai import OpenAI
from rich import print as rprint # Just print prettier
import requests
from PIL import Image
from io import BytesIO

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": "재귀 호출에 대하여 한국어로 설명해 줘."
        }
    ]
)

content = completion.choices[0].message.content
rprint(content)

# Generate an Image
response = client.images.generate(
    prompt="A beautiful sunset over the mountains",
    n=2,
    size="1024x1024"
)


print(response.data[0].url)
# Fetch and display the image
image_url = response.data[0].url
image_response = requests.get(image_url)
img = Image.open(BytesIO(image_response.content))
img.show()


def runchatgpt(prompt, model="gpt-4o-mini"):
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return completion.choices[0].message.content.strip()


user_text = '안녕하세요. 함께 참여해 주셔서 감사합니다.'

user_prompt = f'{user_text}를 영어로 번역해줘'
response = runchatgpt(user_prompt)
print(response)
