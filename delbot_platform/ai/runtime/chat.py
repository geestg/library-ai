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

    context = ""
    for message in request.messages:
        if message.role == "system" and "DOCUMENT CONTEXT" in message.content:
            context = message.content.split(
                "DOCUMENT CONTEXT",
                1,
            )[1].strip()

    answer = (
        "Informasi yang relevan tidak ditemukan dalam context."
    )

    question_terms = [
        word.lower().strip("?,.!:;()")
        for word in user_message.split()
        if len(word.strip("?,.!:;()")) > 2
    ]

    paragraphs = [
        paragraph.strip()
        for paragraph in context.split("\n\n")
        if paragraph.strip()
    ]

    scored = []

    for paragraph in paragraphs:
        lowered = paragraph.lower()
        score = sum(
            1
            for term in question_terms
            if term in lowered
        )
        if score > 0:
            scored.append((score, paragraph))

    scored.sort(
        key=lambda item: item[0],
        reverse=True,
    )

    if scored:
        selected = [
            item[1]
            for item in scored[:3]
        ]

        answer = (
            "Berdasarkan dokumen yang ditemukan:\n\n"
            + "\n\n".join(selected)
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

    import os

    host = os.getenv(
        "CHAT_HOST",
        "0.0.0.0",
    )

    port = int(
        os.getenv(
            "CHAT_PORT",
            "8101",
        )
    )

    uvicorn.run(
        app,
        host=host,
        port=port,
    )
