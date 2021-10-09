import json
import requests
import os
import time
from itertools import product
from collections import defaultdict
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))
os.chdir(os.path.dirname(__file__))
TOKEN = os.getenv('BEARER_TOKEN')


def update():
    """Updates the role probabilty in heroes json file
    """
    hero_ids = []
    with open('json/heroes.json', 'r') as heroes:
        data = heroes.read()
    obj = json.loads(data)
    for i in obj['data']['constants']['heroes']:
        hero_ids.append(i['id'])
    for i, hero in enumerate(hero_ids):
        url = f"https://api.stratz.com/api/v1/Hero/{hero}?rank=8"
        r1, r2, r3, r4, r5 = 0, 0, 0, 0, 0
        safe, mid, off, roam = 0, 0, 0, 0
        r = requests.get(url=url, headers={"Authorization": f"Bearer {TOKEN}"})
        r_obj = r.json()
        total_matches = r_obj['heroes'][0]['pickBan']['pick']['matchCount']
        for j in r_obj['heroes'][0]['heroLaneDetail']:
            if j['laneId'] == 1:
                safe = j['matchCount'] / total_matches
            elif j['laneId'] == 2:
                mid = j['matchCount'] / total_matches
            elif j['laneId'] == 3:
                off = j['matchCount'] / total_matches
            else:
                roam = j['matchCount']
        for k in r_obj['heroes'][0]['heroRoleDetail']:
            if k['roleId'] == 0:
                core = k['matchCount'] / total_matches
            elif k['roleId'] == 1:
                support = k['matchCount'] / total_matches
        # safe lane core/hard support
        r1 = safe * core
        r5 = safe * support
        # offlane core/soft support
        r3 = off * core
        r4 = off * support
        # midlane core/roamer
        r2 = mid * core
        r4 += (mid * support)
        obj['data']['constants']['heroes'][i]['roles'] = [r1, r2, r3, r4, r5]
        print(f"Roles for hero {hero} added successfully!")
        time.sleep(1)
    with open('json/heroes.json', 'w') as heroes:
        json.dump(obj, heroes)


def guess(team):
    """Somewhat of a lazy implementation of guessing lineup based on role probability

    :param team: unsorted array
    :type team: array
    :return: sorted array
    :rtype: array
    :return: -1(unlikely), 0(likely) and 1(highly likely)
    :rtype: int
    """
    likelihood = 1
    original = team.copy()
    dupe = team.copy()
    guessed = [None for i in range(5)]
    with open('json/heroes.json', 'r') as heroes:
        data = heroes.read()
    obj = json.loads(data)
    for i, x in product(obj['data']['constants']['heroes'], range(0, 5)):  # adds role data to each hero
        if i['id'] == team[x]:
            team[x] = (team[x], i['roles'])
    rp = [[] for _ in range(5)]
    for i, x in product(team, range(0, 5)):
        rp[x].append((i[0], i[1][x]))
    for i, x in product(original, range(0, 5)):
        rp[x].sort(reverse=True, key=lambda x: x[1])  # sorts hero ids from highest to lowest probability
        if i == rp[x][0][0]:  # if hero id from original matches the hero id from
            guessed[x] = i
            if i in dupe:
                dupe.remove(i)
    if len(dupe) == 1:  # makes swap based on the role probability
        likelihood = 0
        D = defaultdict(list)
        for i, item in enumerate(guessed):
            D[item].append(i)
        D = {k: v for k, v in D.items() if len(v) > 1}  # heroid followed by the duplicate indices occupied
        i1, i2 = list(D.values())[0][0], list(D.values())[0][1]  # duplicate index 1 and 2 of guessed list
        i1_rp, i2_rp = [y[0] for y in rp[i1]].index(dupe[0]), [y[0] for y in rp[i2]].index(dupe[0])  # index of duplicate hero in tuples in lists i1, i2
        i1_prob, i2_prob = rp[i1][i1_rp][1], rp[i2][i2_rp][1]  # probabilities from tuple i1_rp and i2_rp based on list 0-4 (i1 and i2)
        if i1_prob > i2_prob:
            guessed[i1] = dupe[0]
        else:
            guessed[i2] = dupe[0]
    elif len(dupe) > 1:  # too many duplicates to reliably guess roles
        return original, -1
    return guessed, likelihood


if __name__ == "__main__":
    update()
    # print(guess([65, 21, 45, 121, 41]))
