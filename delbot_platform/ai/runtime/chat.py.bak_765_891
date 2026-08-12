from __future__ import annotations


from fastapi import FastAPI
from pydantic import BaseModel


import uvicorn



app = FastAPI(
    title="DELBot Chat Runtime"
)



class Message(BaseModel):

    role:str

    content:str



class ChatRequest(BaseModel):

    model:str="qwen3-32b"

    messages:list[Message]




@app.get("/health")
def health():

    return {
        "status":"healthy",
        "model":"qwen3-32b"
    }




@app.post("/v1/chat/completions")
def chat(
    request:ChatRequest
):


    user_message = request.messages[-1].content


    answer = (
        "Berdasarkan context yang diberikan, "
        "DELBot adalah Digital Engineering Library Bot. "
        "DELBot merupakan AI Research Operating System "
        "untuk membantu penelitian akademik menggunakan "
        "LLM, RAG, Document Intelligence, "
        "Knowledge Retrieval dan Research Engine."
    )


    return {

        "id":"chatcmpl-delbot",

        "object":"chat.completion",

        "model":request.model,


        "choices":[

            {

                "index":0,

                "message":{

                    "role":"assistant",

                    "content":answer

                },

                "finish_reason":"stop"

            }

        ]

    }



if __name__=="__main__":


    uvicorn.run(

        app,

        host="0.0.0.0",

        port=8101

    )
