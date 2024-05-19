import requests
import aiohttp
import config_data.module_generation_prmt as prmt

async def ai_generate_module(text: str):
    prompt = {
        "modelUri": "gpt://b1gfks0khjkqtiosesft/yandexgpt", #-lite",
        "completionOptions": {
            "stream": False,
            "temperature": 0.3,
            "maxTokens": "2000"
        },
        "messages": [
            *prmt.messages,
            {
                "role": "user", 
                "text": text
            },
        ]
    }

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion" #Async"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Api-Key AQVNxR6zGEOE6NwZxLzAg__WTaw2R788WOjcY1Dk"
    }

    async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=prompt) as response:
                if response.status == 200:
                    result = await response.json()
                    return result['result']['alternatives'][0]['message']['text']
                else:
                    response_text = await response.text()
                    raise Exception(
                        f"Failed to send completion request. "
                        f"Status code: {response.status}"
                        f"\n{response_text}"
                    )

    # response = requests.post(url, headers=headers, json=prompt)
    # response = await requests.get()

    # print(response.json())

    # # convert string to json
    # result = response.json()['result']['alternatives'][0]['message']['text']

    # return result