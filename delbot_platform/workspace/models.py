from __future__ import annotations


from dataclasses import dataclass, field
from datetime import datetime



@dataclass
class ConversationMessage:


    role:str

    content:str

    created_at:str = field(
        default_factory=lambda:
        datetime.utcnow().isoformat()
    )



@dataclass
class ResearchSession:


    session_id:str

    title:str


    messages:list[ConversationMessage] = field(
        default_factory=list
    )


    metadata:dict = field(
        default_factory=dict
    )


    created_at:str = field(
        default_factory=lambda:
        datetime.utcnow().isoformat()
    )
