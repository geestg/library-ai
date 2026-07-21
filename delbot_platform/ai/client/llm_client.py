from __future__ import annotations


import requests



class LLMClient:



    def __init__(

        self,

        url="http://localhost:11435/v1/chat/completions"

    ):

        self.url=url



    def chat(

        self,

        prompt:str,

        model="Qwen3-30B"

    ):


        response=requests.post(

            self.url,

            json={

                "model":model,

                "messages":[

                    {

                        "role":"system",

                        "content":
                        "You are DELBot, an academic research assistant. Answer using provided sources and include citations."

                    },

                    {

                        "role":"user",

                        "content":prompt

                    }

                ],

                "temperature":0.2,

                "max_tokens":2048

            },

            timeout=1200

        )


        response.raise_for_status()


        data=response.json()


        return data["choices"][0]["message"]["content"]
