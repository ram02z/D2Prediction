import json
from graphql import MissingDetails
import requests
from requests.utils import quote
import os
from add_role import guess
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))
os.chdir(os.path.dirname(__file__))
KEY = os.getenv('STEAM_API_KEY')


def patch_odota():
    """Gets Opendota constant information for patches

    :raises MissingDetails: request exception
    :return: json response
    :rtype: str
    """
    url = f"https://api.opendota.com/api/constants/patch"
    try:
        r = requests.get(url=url)
        r_obj = r.json()
        if not r_obj:
            raise MissingDetails("No patch numbers returned.", "Opendota API Constants", str(r.headers))
        return r_obj
    except requests.exceptions.RequestException as e:  # todo: checks the opendota limit header and returns smth
        raise MissingDetails(f"Too many requests.", "Opendota API Constants")


def sql_query(query):
    """Gets response from opendota explorer endpoint based on query parameter

    :param query: SQL query
    :type query: str
    :raises MissingDetails: query error
    :raises MissingDetails: request exception
    :return: json response
    :rtype: str
    """
    url = f"https://api.opendota.com/api/explorer?sql={quote(query)}"
    try:
        r = requests.get(url=url)
        r_obj = r.json()
        if r_obj['err'] is not None:
            raise MissingDetails(f"Query error.", f"{r_obj['err']}", str(r.headers))
        return r_obj
    except requests.exceptions.RequestException as e:  # todo: checks the opendota limit header and returns smth
        raise MissingDetails(f"Too many requests.", "Opendota API Explorer")


def get_live():
    """Gets live match details from valves match api endpoint

    :raises MissingDetails: No live games returned.
    :raises MissingDetails: Too many requests
    :raises MissingDetails: Json parse error
    :return: json response
    :rtype: str
    """
    url = f"https://api.steampowered.com/IDOTA2Match_570/GetTopLiveGame/v1/?key={KEY}&partner=0&format=json"
    req_headers = {'User-Agent': 'Python script'}
    try:
        r = requests.get(url=url, headers=req_headers, data=None)
        r_obj = r.json()
        if not r_obj:
            raise MissingDetails("No live games returned.", "Dota API GetTopLiveGame", str(r.headers))
        return r_obj
    except requests.exceptions.RequestException as e:
        raise MissingDetails("Too many requests.", "Dota API GetTopLiveGame")
    except ValueError:
        raise MissingDetails("Json parse error.", "Dota API GetTopLiveGame")


def get_match(match_id):
    """Gets parameter specific match details from valves match api endpoint

    :param match_id: dota match id
    :type match_id: int
    :raises MissingDetails: empty json object
    :raises MissingDetails: misc result error
    :raises MissingDetails: request exception
    :return: json response
    :rtype: str
    """
    url = f"http://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/v1?match_id={match_id}&key={KEY}"
    req_headers = {'User-Agent': 'Python script'}
    try:
        r = requests.get(url=url, headers=req_headers, data=None)
        r_obj = r.json()
        if not r_obj:
            raise MissingDetails("Missing match details.", "Dota API GetMatchDetails", str(r.headers))
        elif 'error' in r_obj['result']:
            raise MissingDetails(str(r_obj['result']['error']), "Dota API GetMatchDetails", str(r.headers))
        return r_obj
    except requests.exceptions.RequestException as e:
        raise MissingDetails("Too many requests.", "Dota API GetMatchDetails")


def assign_badge(mmr):
    """Returns medal based on param

    :param mmr: MMR value
    :type mmr: int
    :return: medal file name
    :rtype: str
    """
    if mmr >= 8800:
        return "medal_c"
    elif mmr >= 8000:
        return "medal_b"
    else:
        return "medal_a"


def filter_live():
    """Filters live games based on criteria

    :return: json object with live games
    :rtype: str
    """
    matches = []
    r_obj = get_live()
    MAX_TIME = 900  # 15 minutes
    MAX_LEAD = 2500
    for i in r_obj['game_list']:
        heroID_flag = False  # checks if any hero ids are equal to zero
        if i['lobby_type'] == 7 and i['game_time'] > 10 and i['game_time'] < MAX_TIME and i['radiant_lead'] < MAX_LEAD and i['radiant_lead'] > -(MAX_LEAD):
            match = {
                'radiant_team': {},
                'dire_team': {}
            }
            radiant_heroes, dire_heroes = ([] for i in range(2))
            match['server_id'] = i['server_steam_id']
            match['match_id'] = i['match_id']
            match['average_mmr'] = i['average_mmr']
            match['medal'] = f"{assign_badge(i['average_mmr'])}"
            match['time_remaining'] = MAX_TIME - i['game_time']
            match['radiant_vote'] = None
            match['radiant_outcome'] = None
            for j, k in zip(range(0, 5), range(5, 10)):
                if i['players'][j]['hero_id'] == 0 or i['players'][k]['hero_id'] == 0:
                    heroID_flag = True
                radiant_heroes.append(i['players'][j]['hero_id'])
                dire_heroes.append(i['players'][k]['hero_id'])
            print(radiant_heroes, dire_heroes)
            if not heroID_flag:
                match['radiant_team']['heroes'], match['radiant_likelihood'] = guess(radiant_heroes)
                match['dire_team']['heroes'], match['dire_likelihood'] = guess(dire_heroes)
                matches.append(match)
    return matches


def random_matches(patch=None):
    """Selects about 10% random match ids from opendota's match table, returns first 150 rows.
    Match ids are from current patch if patch param is empty or invalid.

    :param patch: dota patch number
    :type patch: str
    :return: random match ids from current patch pro games
    :rtype: array
    """
    matches = []
    patch_res = patch_odota()
    patch_list = [d['name'] for d in patch_res if 'name' in d]
    if patch is None or patch not in patch_list:
        patch = patch_list[-1]
    rand_query = f'''
    SELECT
    matches.match_id
    FROM matches TABLESAMPLE BERNOULLI(10)
    JOIN match_patch using(match_id)
    WHERE TRUE
    AND matches.duration >= 900
    AND match_patch.patch = '{patch}'
    LIMIT 150
    '''
    r_obj = sql_query(rand_query)
    for i in r_obj['rows']:
        if i['match_id'] not in matches:
            matches.append(i['match_id'])
    return matches


if __name__ == "__main__":
    matches = random_matches('7.27')
    print(json.dumps(matches, indent=2))
