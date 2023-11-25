from sqlmodel import Session, select
from fastapi import Depends, HTTPException, status
from api.database.session import getSession
from api.database.models import LeagueChampion, LeagueSkill, LeagueSkin
from api.lol.champion.schemas import Champion

status_code = status.HTTP_202_ACCEPTED
summary = "Update League of legends Champion"


async def endpoint(name: str, body: Champion, db: Session = Depends(getSession)):
    """
    ***Create or update a champion in the league.***

    Args:
    - name (str): The name of the champion.
    - body (Champion): The data to update the champion with.
    - db (Session, optional): The database session. Defaults to Depends(getSession).

    Raises:
        HTTPException: If the champion is not found.

    Returns:
        None
    """
    # select the champion
    query = select(LeagueChampion).where(LeagueChampion.name == name)
    champion: LeagueChampion | None = db.exec(query).first()
    if not champion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    champion.skins = [LeagueSkin(**x.dict()) for x in body.skins]
    champion.abilities = [LeagueSkill(**x.dict()) for x in body.abilities]
    champion.name = body.name
    champion.subtitle = body.subtitle
    champion.role = body.role
    db.add(champion)
    db.commit()
