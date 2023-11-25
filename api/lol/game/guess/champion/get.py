from api.database.session import getSession
from sqlmodel import Session, select, func
import random
from api.database.models import LeagueChampion, LeagueSkill, LeagueSkin
from api.lol.game.guess.champion.schemas import GuessTheChampion
from fastapi import Depends


async def endpoint(db: Session = Depends(getSession)):
    random_champions: list[LeagueChampion] = [
        x
        for x in db.exec(select(LeagueChampion).order_by(func.random()).limit(10)).all()
    ]
    champion_int: int = random.randint(0, 8)
    answer: str = random_champions[champion_int].name
    choices: list[str] = [
        answer,
        *[random_champions[random.randint(0, 9)].name for _ in range(3)],
    ]
    random.shuffle(choices)
    return GuessTheChampion(
        image=random_champions[champion_int].skins[0].image,
        choices=choices,
        description=random_champions[champion_int]
        .description.lower()
        .replace(answer, "*" * 10),
        answer=answer,
    )
