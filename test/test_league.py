import json
import os
from fastapi.testclient import TestClient
from httpx import Response
import httpx
from bs4 import BeautifulSoup
from api.main import app
from urllib.parse import urlencode


class TestLeague:
    """
    This class represents the test cases for the League API.
    """

    client: TestClient = TestClient(app)
    champion_names: list[str] = []


class TestChampion(TestLeague):
    """
    This class contains test cases for the champion API.
    """

    def fetch_champion_names(self):
        """
        Fetches the names of the champions from the League of Legends website.
        """

        with httpx.Client() as session:
            response: Response = session.get(
                "https://www.leagueoflegends.com/en-ph/champions/"
            )
            soup = BeautifulSoup(response.text, "html.parser")
            self.champion_names: list[str] = [
                x.find("span").text
                for x in soup.findAll(
                    "span", {"class": "style__Name-sc-n3ovyt-2 fHdhXn"}
                )
            ]

    def test_post(self):
        """
        Test case to check the POST endpoint of the champion API.
        """

        self.fetch_champion_names()
        json_files: list[dict] = []
        for name in self.champion_names:
            file_name: str = (
                name.replace(" ", "-")
                .replace("'", "-")
                .replace(".", "")
                .replace("Nunu-&-Willump", "nunu")
                .replace("Renata-Glasc", "renata")
            )
            with open(f"{os.getcwd()}/league/{file_name}.json", "r") as f:
                json_files.append(json.loads(f.read()))
        for file in json_files:
            response = self.client.post("/lol/champion/", json=file)
            assert response.status_code == 201 or response.status_code == 409

    def test_get(self):
        """
        Test case to check the GET endpoint of the champion API.
        """

        self.fetch_champion_names()
        for name in self.champion_names:
            query_params: str = urlencode({"name": name.lower()})
            response: Response = self.client.get(f"/lol/champion/?{query_params}")
            assert response.status_code == 200, f"Error in get {query_params}"
