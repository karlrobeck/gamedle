import json
import os
import time
from bs4 import BeautifulSoup
import requests
from bs4 import BeautifulSoup


def scrape_champion(link: str):
    with requests.Session() as session:
        response = session.get(link)
        print(response.status_code)
    html = BeautifulSoup(response.text, "html.parser")

    name = html.find("span", {"data-testid": "overview:title"}).text  # type: ignore
    subtitle = html.find("span", {"data-testid": "overview:subtitle"}).text  # type: ignore
    role = html.find("div", {"data-testid": "overview:role"}).text  # type: ignore
    description = html.find("p", {"data-testid": "overview:description"}).text  # type: ignore

    img_abilities = [
        x.find("img").attrs["src"]
        for x in html.find(
            "div", {"class": "style__OptionList-sc-1ac4kmt-3 ipfewp"}
        ).findAll(  # type: ignore
            "button"
        )  # type: ignore
    ]
    li_abilities = [
        (x.find("h6").text, x.find("h5").text, x.find("p").text)  # type: ignore
        for x in [
            html.find("li", {"data-testid": f"abilities:ability-{x}"}) for x in range(4)
        ]
    ]
    skin_images = [
        x.find("img").attrs["src"]  # type:ignore
        for x in html.find(
            "div", {"class": "style__Slideshow-sc-gky2mu-2 bQSHcx"}
        )  # type:ignore
    ]
    skin_names = [
        x.find("label").text
        for x in html.find(
            "ul",
            {"class": "style__CarouselContainer-sc-gky2mu-11 jOxjfS"},
        ).findAll(  # type: ignore
            "li"
        )  # type:ignore
    ]

    output: dict[str, str | list] = {
        "name": name,
        "subtitle": subtitle,
        "role": role,
        "description": description,
        "abilities": [
            {"position": text[0], "name": text[1], "description": text[2], "image": img}
            for text, img in zip(li_abilities, img_abilities)
        ],
        "skins": [
            {"name": name, "image": img} for name, img in zip(skin_names, skin_images)
        ],
    }
    return output


if __name__ == "__main__":
    with requests.Session() as session:
        response = session.get("https://www.leagueoflegends.com/en-ph/champions/")

        champion_names: list[str] = [
            x.find("span")
            .text.replace(" ", "-")
            .replace("'", "-")
            .replace(".", "")
            .replace("Nunu-&-Willump", "nunu")
            .replace("Renata-Glasc", "renata")
            for x in BeautifulSoup(response.text, "html.parser").findAll(
                "span", {"class": "style__Name-sc-n3ovyt-2 fHdhXn"}
            )
        ]

    for i, c in enumerate(champion_names):
        if not os.path.exists(f"{os.getcwd()}/league/"):
            os.mkdir(f"{os.getcwd()}/league/")
        if not os.path.exists(f"{os.getcwd()}/league/{c}.json"):
            print(f"scraping {c}")
            data = json.dumps(
                scrape_champion(f"https://www.leagueoflegends.com/en-ph/champions/{c}/")
            )
            with open(f"{os.getcwd()}/league/{c}.json", "x+") as f:
                f.write(data)
            if i % 50 == 0 and i != 0:
                print("sleeping...")
                time.sleep(60)

        else:
            print(f"skipping {c}")
    json_files = []
    # os.system(f"python {os.getcwd()}/api/database/models.py")
    for file in os.listdir(f"{os.getcwd()}/league/"):
        with open(f"{os.getcwd()}/league/{file}", "r") as f:
            json_files.append(json.loads(f.read()))
    for x in json_files:
        print(requests.post("http://127.0.0.1:8000/lol/champion/", json=x).text)
