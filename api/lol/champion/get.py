from fastapi import Depends, status, HTTPException
from sqlmodel import Session, select
from lol.champion.schemas import Champion, ChampionAbilities, ChampionSkin
from database.session import getSession
from database.models import LeagueChampion, LeagueSkill, LeagueSkin


async def endpoint(name: str, db: Session = Depends(getSession)) -> Champion:
    if not db.exec(select(LeagueChampion).where(LeagueChampion.name == name)).first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=("Champion not found")
        )

    champion_info_query = select(LeagueChampion).where(LeagueChampion.name == name)
    champion: LeagueChampion = db.exec(champion_info_query).one()
    champion_ability_query = select(LeagueSkill).where(
        LeagueSkill.champion_id == champion.id
    )
    champion_skin_query = select(LeagueSkin).where(
        LeagueSkin.champion_id == champion.id
    )

    abilities = db.exec(champion_ability_query).all()
    skins = db.exec(champion_skin_query).all()
    return Champion(
        **champion.dict(),
        abilities=[ChampionAbilities(**x.dict()) for x in abilities],
        skins=[ChampionSkin(**x.dict()) for x in skins]
    )
