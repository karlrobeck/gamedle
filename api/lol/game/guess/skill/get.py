import random
from fastapi import Depends
from sqlmodel import Session, select
from sqlalchemy.sql.expression import func
from api.lol.game.guess.skill.schemas import GuessTheSkill
from api.database.models import LeagueChampion

from api.database.session import getSession


async def endpoint(db: Session = Depends(getSession)):
    # get random champion from the database
    random_champions: list[LeagueChampion] = [
        x
        for x in db.exec(select(LeagueChampion).order_by(func.random()).limit(10)).all()
    ]
    champion_int: int = random.randint(0, 8)
    answer_int: int = random.randint(0, 3)
    answer: str = random_champions[champion_int].abilities[answer_int].name
    choices: list[str] = [
        answer,
        *[
            random_champions[random.randint(0, 9)].abilities[random.randint(0, 3)].name
            for _ in range(3)
        ],
    ]
    random.shuffle(choices)
    return GuessTheSkill(
        image=random_champions[champion_int].abilities[answer_int].image,
        choices=choices,
        description=random_champions[champion_int].abilities[answer_int].description,
        answer=answer,
    )
