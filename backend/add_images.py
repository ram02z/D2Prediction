import json
import os
os.chdir(os.path.dirname(__file__))


def update():
    """
    Updates the heroes json file with the image links directly from dota's cdn.
    read drafts/todo.txt for more info
    """
    with open('json/heroes.json', 'r') as heroes:
        data = heroes.read()
    obj = json.loads(data)
    changes = 0
    for i in obj['data']['constants']['heroes']:
        if 'shortName' in i:
            i['shortName'] = f"http://cdn.dota2.com/apps/dota2/images/heroes/{i['shortName']}_full.png"
            i["image_url"] = i.pop("shortName")
            changes += 1
    if changes:
        with open('json/heroes.json', 'w') as heroes:
            json.dump(obj, heroes)
        print(f"{changes} hero image(s) added.")
    else:
        print("Hero images up to date.")


if __name__ == "__main__":
    update()
