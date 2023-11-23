from pydantic import BaseModel


class ChampionAbilities(BaseModel):
    position: str
    name: str
    description: str
    image: str


class ChampionSkin(BaseModel):
    name: str
    image: str


class Champion(BaseModel):
    name: str
    subtitle: str
    role: str
    description: str
    abilities: list[ChampionAbilities]
    skins: list[ChampionSkin]
