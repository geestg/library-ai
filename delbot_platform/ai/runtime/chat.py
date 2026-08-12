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

    system_text = "\n".join(
        message.content
        for message in request.messages
        if message.role == "system"
    ).lower()

    conversation_mode = (
        "mode: conversation" in system_text
    )

    research_mode = (
        "mode: research" in system_text
    )

    if conversation_mode:
        lowered = user_message.lower().strip()

        if any(
            greeting in lowered
            for greeting in (
                "hai",
                "halo",
                "hello",
                "apa kabar",
            )
        ):
            answer = (
                "Baik. Kamu sendiri bagaimana? "
                "Kalau sedang menyiapkan penelitian, "
                "kita juga bisa mulai dari mencari arah topiknya."
            )
        elif any(
            term in lowered
            for term in (
                "terima kasih",
                "makasih",
                "thanks",
            )
        ):
            answer = (
                "Sama-sama. Kita lanjutkan ketika kamu "
                "sudah siap membahas penelitian."
            )
        else:
            answer = (
                "Saya siap membantu. "
                "Kalau pembicaraan mulai masuk ke penelitian, "
                "kita bisa mempersempit topik dan arah penelitian "
                "terlebih dahulu sebelum menggunakan evidence repository."
            )

        return {
            "id": "chatcmpl-delbot",
            "object": "chat.completion",
            "model": request.model,
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": answer,
                    },
                    "finish_reason": "stop",
                }
            ],
        }

    if research_mode and not context.strip():
        lowered = user_message.lower().strip()

        if (
            "ai" in lowered
            or "artificial intelligence" in lowered
            or "kecerdasan buatan" in lowered
        ):
            answer = (
                "AI cukup luas. Untuk mempersempit arah penelitian, "
                "kamu bisa mempertimbangkan:\n\n"
                "- AI untuk pendidikan atau kampus\n"
                "- Computer Vision\n"
                "- NLP atau LLM\n"
                "- AI untuk biologi\n"
                "- AI untuk penelitian atau akademik\n"
                "- bidang AI lain yang sesuai minatmu\n\n"
                "Pilih satu arah yang paling menarik, lalu kita "
                "bisa lanjut mencari penelitian yang relevan dari repository."
            )
        elif (
            "computer vision" in lowered
            or "computer-vision" in lowered
        ):
            answer = (
                "Computer Vision bisa menjadi arah penelitian yang "
                "lebih spesifik. Kita dapat mempersempitnya lagi "
                "berdasarkan objek, masalah, dataset, atau metode "
                "yang ingin digunakan. Setelah arahnya cukup jelas, "
                "DELBot dapat mencari penelitian yang relevan dari repository."
            )
        else:
            answer = (
                "Topiknya sudah mulai masuk ke penelitian, tetapi "
                "belum perlu mengambil evidence dari repository. "
                "Mari persempit terlebih dahulu bidang, objek, masalah, "
                "atau arah penelitian yang ingin kamu dalami."
            )

        return {
            "id": "chatcmpl-delbot",
            "object": "chat.completion",
            "model": request.model,
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": answer,
                    },
                    "finish_reason": "stop",
                }
            ],
        }

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
            "8107",
        )
    )

    uvicorn.run(
        app,
        host=host,
        port=port,
    )
