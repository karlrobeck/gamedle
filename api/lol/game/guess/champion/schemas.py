from pydantic import BaseModel


class GuessTheChampion(BaseModel):
    image: str
    description: str
    choices: list[str]
    answer: str
