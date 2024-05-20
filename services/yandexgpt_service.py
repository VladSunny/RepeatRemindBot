import requests
import aiohttp
import config_data.module_generation_prmt as prmt
import json
import re

async def ai_generate_module(text: str) -> dict[str, str]:

    def extract_json_from_response(response):
        # Регулярное выражение для нахождения JSON
        json_pattern = r'\{.*?\}'
        match = re.search(json_pattern, response, re.DOTALL)
        if match:
            json_str = match.group(0)
            try:
                json_data = json.loads(json_str)
                return json_data
            except json.JSONDecodeError as e:
                print("Error decoding JSON:", e)
        else:
            print("No JSON found in the response")
        return None

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
                    return extract_json_from_response(result['result']['alternatives'][0]['message']['text'])
                else:
                    response_text = await response.text()
                    raise Exception(
                        f"Failed to send completion request. "
                        f"Status code: {response.status}"
                        f"\n{response_text}"
                    )
