from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, wait
from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select
from lol.champion.schemas import Champion
from database.session import getSession
from database.models import LeagueChampion, LeagueSkill, LeagueSkin
from uuid import uuid1


async def endpoint(body: Champion, db: Session = Depends(getSession)) -> str:
    # generate unique uuid
    id: str = str(uuid1())
    body.name = body.name.lower()

    if db.exec(select(LeagueChampion).where(LeagueChampion.name == body.name)).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=("Champion already exists")
        )

    for skin in body.skins:
        if db.exec(select(LeagueSkin).where(LeagueSkin.name == skin.name)).first():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=("Champion Skin already exists"),
            )

    for ability in body.abilities:
        if db.exec(select(LeagueSkill).where(LeagueSkill.name == ability.name)).first():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=("Champion Ability already exists"),
            )
    abilities = [
        LeagueSkill(
            id=str(uuid1()),
            position=x.position,
            name=x.name,
            description=x.description,
            image=x.image,
            champion_id=id,
        )
        for x in body.abilities
    ]
    skins = [
        LeagueSkin(id=str(uuid1()), name=x.name, image=x.image, champion_id=id)
        for x in body.skins
    ]
    db.add(
        LeagueChampion(
            id=id,
            subtitle=body.subtitle,
            name=body.name,
            role=body.role,
            description=body.description,
            skins=skins,
            abilities=abilities,
        )
    )
    db.commit()
    return f"Champion {body.name} created"
