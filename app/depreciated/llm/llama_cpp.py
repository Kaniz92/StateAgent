
from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

class LLM:
    # TODO: add implementation
    # TODO: Add a parent class to make llm call generic

    def generate(self, prompt:str) -> str:
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        messages = [
            {"role": "system", "content": prompt}
        ]
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.2,
            max_tokens=256,
            frequency_penalty=0.0
        )

        text = response.choices[0].message.content

        ======
        llm = LlamaAPI(llama_api_token)
        llm.predict(prompt)

        return text


