from typing import List
from sqlalchemy import table
from sqlmodel import Field, Relationship, SQLModel, create_engine
import sys


class LeagueSkin(SQLModel, table=True):
    id: str = Field(primary_key=True)
    name: str = Field(unique=True)
    image: str
    champion_id: str = Field(foreign_key="leaguechampion.id")
    champion: List["LeagueChampion"] = Relationship(back_populates="skins")


class LeagueSkill(SQLModel, table=True):
    id: str = Field(primary_key=True)
    position: str
    name: str = Field(unique=True)
    description: str
    image: str
    champion_id: str = Field(foreign_key="leaguechampion.id")
    champion: List["LeagueChampion"] = Relationship(back_populates="abilities")


class LeagueChampion(SQLModel, table=True):
    id: str = Field(primary_key=True)
    name: str = Field(unique=True)
    subtitle: str
    role: str
    description: str
    abilities: List[LeagueSkill] = Relationship(back_populates="champion")
    skins: List[LeagueSkin] = Relationship(back_populates="champion")


engine = create_engine(
    "sqlite:///./gamedle.db",
    echo=True,
    connect_args={"check_same_thread": False},
)

if __name__ == "__main__":
    SQLModel.metadata.create_all(engine)
