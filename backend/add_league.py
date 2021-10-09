import json
import requests
import shutil
import os
os.chdir(os.path.dirname(__file__))


def new():
    """Creates a new entry for a league in the json file.

    :raises ValueError: League ID already exists in json file
    """
    with open('json/leagues.json', 'r') as jfile:
        data = jfile.read()
    obj = json.loads(data)
    while True:
        try:
            league_id = int(input("League ID:"))
            for i in obj['leagues']:
                if i['id'] == league_id:
                    print("Already exists.")
                    raise ValueError
            league_name = input("League Name:")
            league_version = input("League version:")
            banner_url = f"https://cdn.stratz.com/images/dota2/leagues/{league_id}.png"
            r = requests.get(banner_url, stream=True)
            if r.status_code == 404:
                league_banner = "default.png"
            elif r.status_code == 200:
                with open(f"static/images/league_banners/{league_id}.png", 'wb') as f:
                    shutil.copyfileobj(r.raw, f)
                league_banner = f"{league_id}.png"
            del r
            entry = {
                'ids': {},
            }
            # adds to entry
            easy, medium, hard, black_list = ([] for _ in range(4))
            entry['id'], entry['name'], entry['banner'], entry['version'], entry['ids']['easy'], entry['ids']['medium'], entry['ids']['hard'], entry['black_list'] = league_id, league_name, league_banner, league_version, easy, medium, hard, black_list
            obj['leagues'].append(entry)
            with open('json/leagues.json', 'w') as leagues:
                json.dump(obj, leagues)
            print(f"{league_id} has been added.")
            agane = input("Add another? Press enter to exit.")
            if not agane:
                break
        except ValueError:
            print("Oops.")


def fix():
    with open('json/leagues.json', 'r') as jfile:
        data = jfile.read()
    obj = json.loads(data)
    for i in obj['leagues']:
        easy, medium, hard = i['easy_ids'], i['medium_ids'], i['hard_ids']
        entries_to_remove = ('easy_ids', 'medium_ids', 'hard_ids')
        for k in entries_to_remove:
            i.pop(k, None)
        i['ids'] = {'easy': easy, 'medium': medium, 'hard': hard}
    with open('json/leagues.json', 'w') as leagues:
        json.dump(obj, leagues)


if __name__ == "__main__":
    new()
