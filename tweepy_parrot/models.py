from typing import Dict, Set

from pydantic import BaseModel


class ParrotData(BaseModel):
    seen_tweets: Set[str]
    markov_chain: Dict[str, Dict[str, int]]

    class Config:
        json_encoders = {
            Set: lambda s: list(s),
        }