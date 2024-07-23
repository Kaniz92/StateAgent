
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

        #
        # =======
        # davinci = OpenAI(model_name='text-davinci-003')
        # llm_chain = LLMChain(
        #     prompt=prompt,
        #     llm=davinci
        # )
        #
        # response = llm_chain.run(prompt)
        #
        #
        #
        #


        # =====
        # llama_api_token = os.getenv('LLAMA_API_TOKEN')
        # llama = LlamaAPI(llama_api_token)
        #
        # api_request_json = {
        #     "model": "llama3-70b",
        #     "messages": [
        #         {"role": "system",
        #          'content': prompt},
        #     ],
        #     "temperature" : 0.1
        # }
        #
        # # Make your request and handle the response
        # response = llama.run(api_request_json)
        # text = json.dumps(response.json(), indent=2)
        #
        # # response = llama.create_chat_completion(
        # #     messages = [{
        # #         'role': 'system',
        # #         'content': prompt
        # #     }],
        # #     temperature = 0.1
        # # )
        # #

        return text


