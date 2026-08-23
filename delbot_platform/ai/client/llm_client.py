from __future__ import annotations

import requests



class LLMClient:


    def __init__(
        self,
        url="http://localhost:11435/v1/chat/completions",
        model="/workspace/Qwen3-30B-MoE"
    ):

        self.url=url
        self.model=model



    def chat(
        self,
        messages:list[dict],
        temperature:float=0.2,
        max_tokens:int=800
    ):


        payload={

            "model":self.model,

            "messages":messages,

            "temperature":temperature,

            "max_tokens":max_tokens

        }


        print("="*50)
        print("[LLM REQUEST]")
        print(payload)
        print("="*50)



        response=requests.post(

            self.url,

            json=payload,

            timeout=900

        )


        if response.status_code != 200:

            print(response.text)



        response.raise_for_status()


        data=response.json()


        return data["choices"][0]["message"]["content"]
