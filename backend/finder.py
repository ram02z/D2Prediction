import requests
import json


def findmatch(a, b):
    teama = "&".join(map(lambda p: f"teamA={p}", a))
    teamb = "&".join(map(lambda p: f"teamB={p}", b))
    url = f"https://api.opendota.com/api/findMatches?{teama}&{teamb}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        if response.status_code == 200:
            matches = response.json()
            print(matches)
    except requests.exceptions.Timeout as e:
        print("Opendota API down", e)


def h2id(hero_name):
    hID = None
    with open('json/heroes.json', 'r') as heroids:
        data = heroids.read()
    obj = json.loads(data)
    for i in obj['data']['constants']['heroes']:
        for a, v in i.items():
            if a == "localized_name" and v == hero_name:
                hID = i["id"]
    return hID


if __name__ == '__main__':
    teama = []
    teamb = []
    for i in range(5):
        while True:
            hero = input(f"Radiant hero {i+1}:")
            hID = h2id(hero.title())
            if hID and hID not in teama:
                teama.append(hID)
                break
            else:
                print("Invalid hero/hero already in match.")
                continue
    for i in range(5):
        while True:
            hero = input(f"Dire hero {i+1}:")
            hID = h2id(hero.title())
            if hID and hID not in teama and hID not in teamb:
                teamb.append(hID)
                break
            else:
                print("Invalid hero/hero already in match.")
                continue
    findmatch(teama, teamb)
