from fastapi import HTTPException


def handle_llm_error(error):

    raise HTTPException(

        status_code=500,

        detail=f"LLM Error: {str(error)}"
    )