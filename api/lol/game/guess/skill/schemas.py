from pydantic import BaseModel


class GuessTheSkill(BaseModel):
    image: str
    description: str
    choices: list[str]
    answer: str
