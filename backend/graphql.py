import requests
import json
import os
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))
os.chdir(os.path.dirname(__file__))
TOKEN = os.getenv('BEARER_TOKEN')


class MissingDetails(Exception):
    """Response is missing X details.

    :param Exception: NoneType is returned
    :type Exception: AttributeError
    :return: Reason why the exception was raised
    :rtype: str
    """
    def __init__(self, message, payload=None, headers=None):
        self.message = message
        self.payload = payload
        self.headers = headers

    def __str__(self):
        return str(self.message)


def version_name(version_id, constants):
    """Converts the version id to the display name using constants dictionary

    :param version_id: integer value of the game version
    :type version_id: int
    :param constants: dictionary containing the game version ids and display names
    :type constants: str
    :return: game version display name
    :rtype: str
    """
    for i in constants['gameVersions']:
        if i['id'] == version_id:
            return i['name']


def roundup(a):
    """Basically the math ceil function

    :param a: float value
    :type a: float
    :return: rounded float to whole number
    :rtype: int
    """
    return int(a) + ((int(a) - a) != 0)


def percent_inc(a, b):
    """Calculates percentage increase

    :param a: first number
    :type a: float
    :param b: second number
    :type b: float
    :return: value of the percentage increase
    :rtype: float
    """
    return ((a - b) / b) * 100


def hdisplay(h_id):
    """Converts the hero id to hero display name


    :return: hero display name
    :rtype: str
    """
    display_name = str(h_id)
    with open('json/heroes.json', 'r') as heroes:
        data = heroes.read()
    obj = json.loads(data)
    for i in obj['data']['constants']['heroes']:
        for a, v in i.items():
            if a == "id" and v == h_id:
                display_name = i["displayName"]
    return display_name


def match_query(match_id, full=0):
    """Consumes Stratz GraphQL API in order to return relevant information tied to the match_id arg.

    :param match_id: match id
    :type match_id: int
    :param full: is full query?, defaults to 0
    :type full: int, optional
    :return: json object
    :rtype: str
    :return: conditional val
    :rtype: int/boolean
    """
    url = 'https://api.stratz.com/graphql'

    basic_query = """
  query match {
    match(id: %s) {
      id
      didRadiantWin
      durationSeconds
      leagueId
      league {
        displayName
      }
      gameVersionId
      radiantTeam {
        id
        name
      }
      direTeam {
        id
        name
      }
      players {
        heroId
        kills
        lane
        roleBasic
        stats {
          networthPerMinute
        }
      }
    }
    constants {
      gameVersions {
        id
        name
      }
    }
  }
  """ % json.dumps(match_id)

    full_query = """
  query match {
    match(id: %s) {
      id
      didRadiantWin
      durationSeconds
      leagueId
      league {
        displayName
      }
      gameVersionId
      analysisOutcome
      radiantTeam {
        id
        name
      }
      direTeam {
        id
        name
      }
      stats {
        radiantExperienceLeads
        radiantNetworthLeads
      }
      playbackData {
        towerDeathEvents {
          dire
          time
          radiant
        }
      }
      players {
        heroId
        kills
        lane
        roleBasic
        stats {
          networthPerMinute
          heroDamageCount
          lastHitCount
          tripsFountainPerMinute
        }
        playbackData {
          buyBackEvents {
            time
          }
        }
      }
    }
    constants {
      gameVersions {
        id
        name
      }
    }
  }
  """ % json.dumps(match_id)
    try:
        if full:
            r = requests.post(url=url, json={'query': full_query})
        else:
            r = requests.post(url=url, json={'query': basic_query})
        r_obj = r.json()
        if r_obj['data']['match'] is None:
            raise MissingDetails('Match is not available.',
                                 match_id, str(r.headers))
        return r_obj, full
    # todo: checks the stratz limit header and returns smth
    except requests.exceptions.RequestException as e:
        raise MissingDetails(f"Too many requests.", f"{match_id}")


def isParsed(r_obj, full):
    """Ensures that there are no missing details from the response object.

    :param r_obj: json object
    :type r_obj: str
    :param full: is full query?
    :type full: int
    :raises MissingDetails: Values from radiantTeam missing
    :raises MissingDetails: Values from direTeam missing
    :raises MissingDetails: radiantNetworthLeads has missing values
    :raises MissingDetails: radiantExperienceLeads has missing values
    :raises MissingDetails: networthPerMinute missing for player i
    :raises MissingDetails: heroDamageCount missing for player i
    :raises MissingDetails: lastHitCount missing for player i
    :raises MissingDetails: Values from tripsFountainPerMinute missing for player i
    :raises MissingDetails: Misisng misc values for player i
    :return: json object
    :rtype: str
    """
    match_id = r_obj['data']['match']['id']
    if r_obj['data']['match']['radiantTeam'] is None or None in r_obj['data']['match']['radiantTeam'].values():  # basic
        raise MissingDetails(
            f"Values from radiantTeam missing.", f"{match_id}")
    elif r_obj['data']['match']['direTeam'] is None or None in r_obj['data']['match']['direTeam'].values():  # basic
        raise MissingDetails(f"Values from direTeam missing.", f"{match_id}")
    elif full:
        if None in r_obj['data']['match']['stats']['radiantNetworthLeads']:  # full
            raise MissingDetails(
                f"radiantNetworthLeads has missing values", f"{match_id}")
        elif None in r_obj['data']['match']['stats']['radiantExperienceLeads']:  # full
            raise MissingDetails(
                f"radiantExperienceLeads has missing values", f"{match_id}")
    elif r_obj['data']['match']['players']:  # basic
        for i in range(0, 10):
            if r_obj['data']['match']['players'][i]['stats']['networthPerMinute'] is None:  # basic
                raise MissingDetails(
                    f"networthPerMinute missing for player {i}.", f"{match_id}")
            elif full:
                if r_obj['data']['match']['players'][i]['stats']['heroDamageCount'] is None:  # full
                    raise MissingDetails(
                        f"heroDamageCount missing for player {i}.", f"{match_id}")
                elif r_obj['data']['match']['players'][i]['stats']['lastHitCount'] is None:  # full
                    raise MissingDetails(
                        f"lastHitCount missing for player {i}.", f"{match_id}")
                elif None in r_obj['data']['match']['players'][i]['stats']['tripsFountainPerMinute']:  # full
                    raise MissingDetails(
                        f"Values from tripsFountainPerMinute missing for player {i}.", f"{match_id}")
                elif None in r_obj['data']['match']['players'][i].values():  # full
                    # the check is done in add_hints
                    if not r_obj['data']['match']['players'][i]['playbackData'] is None:
                        raise MissingDetails(
                            f"Misisng values for player {i}.", f"{match_id}")
    return r_obj


def team_tuples(team_tuple, team_ids):
    """Creates tuple for every role based on team_tuple and the midlaner is assigned to team_ids

    Args:
        team_tuple (tuple): tuple containing heroId and their analyazed lane, role and networth at 12 minutes
        team_ids (array): array to have ids assigned systemically

    Returns:
        [array]: multiple arrays; team_ids, team_safe, team_off, team_supp and team_roam
    """
    """Creates tuple for every role based on team_tuple and the midlaner is assigned to team_ids
    :param team_tuple: tuple containing heroId and their analyazed lane, role and networth at 12 minutes
    :type team_tuple: tuple
    :param team_ids: array to have ids assigned systemically
    :type team_ids: array
    :return: team_ids, team_safe, team_off, team_supp and team_roam
    :rtype: array
    """
    team_roam = None
    team_safe, team_off, team_supp = ([] for _ in range(3))
    for i in team_tuple:
        if i[1] == 1 and i[2] == 0:  # safe lane core
            team_safe.append(tuple([i[0], i[3]]))
        elif i[1] == 2 and i[2] == 0:  # midlane core
            team_ids[1] = i[0]
        elif i[1] == 3 and i[2] == 0:  # offlane core
            team_off.append(tuple([i[0], i[3]]))
        elif i[2] == 1:  # support
            team_supp.append(tuple([i[0], i[3]]))
        elif i[1] == 0 or i[1] == 4:  # roaming/jungle
            team_roam = i[0]
    return team_ids, team_safe, team_off, team_supp, team_roam


def assign_safe(team_ids, team_safe, team_supp):
    """Assigns the core safe laner to fixed position in team_ids and support safe laner is appended to team_supp

    :param team_ids: array to have ids assigned systemically
    :type team_ids: array
    :param team_safe: array with safe laner(s) and their networth at 12 minutes
    :type team_safe: array
    :param team_supp: array with support(s) and their networth at 12 minutes
    :type team_supp: array
    :return: team_ids and team_supp
    :rtype: array
    """
    if len(team_safe) == 2:
        if team_safe[0][1] > team_safe[1][1]:
            team_ids[0] = team_safe[0][0]
            team_supp.append(team_safe[1])
        else:
            team_ids[0] = team_safe[1][0]
            team_supp.append(team_safe[0])
    elif len(team_safe) == 1:
        team_ids[0] = team_safe[0][0]
    return team_ids, team_supp


def assign_off(team_ids, team_off):
    """Assigns the core and/or support off laner to fixed position(s) in team_ids

    :param team_ids: array to have ids assigned systemically
    :type team_ids: array
    :param team_off: array with offlaner(s) and their networth at 12 minutes
    :type team_off: array
    :return: array with offlaner(s) systemically assigned
    :rtype: array
    """
    if len(team_off) == 2:
        if team_off[0][1] > team_off[1][1]:
            team_ids[2] = team_off[0][0]
            team_ids[3] = team_off[1][0]
        else:
            team_ids[2] = team_off[1][0]
            team_ids[3] = team_off[0][0]
    elif len(team_off) == 1:
        team_ids[2] = team_off[0][0]
    return team_ids


def assign_supp(team_ids, team_supp):
    """Assigns support(s) to fixed position(s) in team_ids

    :param team_ids: array to have ids assigned systemically
    :type team_ids: array
    :param team_supp: array with support(s) and their networth at 12 minutes
    :type team_supp: array
    :return: array with support(s) systemically assigned
    :rtype: array
    """
    if len(team_supp) == 2:
        if team_supp[0][1] > team_supp[1][1]:
            team_ids[3] = team_supp[0][0]
            team_ids[4] = team_supp[1][0]
        else:
            team_ids[3] = team_supp[1][0]
            team_ids[4] = team_supp[0][0]
    elif len(team_supp) == 1:
        team_ids[4] = team_supp[0][0]
    return team_ids


def assign_missing(team_ids, team_roam):
    """Assigns missing role if only one is missing, otherwise None is returned

    :param team_ids: array to have ids assigned systemically
    :type team_ids: array
    :param team_roam: hero id of roamer
    :type team_roam: int
    :raises MissingDetails: more than one hero is missing from team_ids
    :return: array with roamer filling in "empty" position
    :rtype: array
    """
    missing = [index for index in range(
        len(team_ids)) if team_ids[index] is None]
    if len(missing) != 1:
        raise MissingDetails(">1 hero from team missing.", f"{team_ids}")
    if team_roam is not None:
        team_ids[missing[0]] = team_roam
    else:
        return
    return team_ids


def clean_obj(r_obj):
    """Creates a new dictionary, clean, which abstracts details not required.
    Relevant league information is extracted from leagues json file.
    Hero ids for each team are added in the following order (safelane, midlane, offlane, soft support and hard support) based on lane, role and midgame networth.

    :param r_obj: json object
    :type r_obj: str
    :raises MissingDetails: Radiant lineup issue
    :raises MissingDetails: Dire lineup issue
    :return: abstracted dictionary
    :rtype: str
    """
    clean = {
        "id": None,
        "duration": None,
        "radiant_vote": None,
        "radiant_outcome": None,
        "league_name": None,
        "league_banner": None,
        "league_ver": None,
        "radiant_team": {
            "id": None,
            "name": "Radiant",
            "heroes": [
                None,
                None,
                None,
                None,
                None
            ]
        },
        "dire_team": {
            "id": None,
            "name": "Dire",
            "heroes": [
                None,
                None,
                None,
                None,
                None
            ]
        }
    }
    clean['id'] = r_obj['data']['match']['id']
    dseconds = r_obj['data']['match']['durationSeconds']
    midgame_time = int(int(dseconds / 60) / 2)
    clean['duration'] = '{0:02d}:{1:02d}'.format(*divmod(dseconds, 60))
    clean['radiant_outcome'] = r_obj['data']['match']['didRadiantWin']
    with open('json/leagues.json', 'r') as jfile:
        data = jfile.read()
    l_obj = json.loads(data)
    league_id = r_obj['data']['match']['leagueId']
    for i in l_obj['leagues']:
        if i['id'] == league_id:
            clean['league_name'] = i['name']
            clean['league_banner'] = i['banner']
            clean['league_ver'] = i['version']
    if clean['league_name'] is None and r_obj['data']['match']['league'] is not None:
        clean['league_name'] = r_obj['data']['match']['league']['displayName']
        clean['league_banner'] = "league_banners/default.png"
        clean['league_ver'] = version_name(
            r_obj['data']['match']['gameVersionId'], r_obj['data']['constants'])
    clean['radiant_team']['id'] = r_obj['data']['match']['radiantTeam']['id']
    clean['dire_team']['id'] = r_obj['data']['match']['direTeam']['id']
    clean['radiant_team']['name'] = r_obj['data']['match']['radiantTeam']['name']
    clean['dire_team']['name'] = r_obj['data']['match']['direTeam']['name']
    radiant_tuple, dire_tuple = ([] for _ in range(2))
    radiant_ids, dire_ids = clean['radiant_team']['heroes'], clean['dire_team']['heroes']
    # creates tuple containing heroId and their analyazed lane, role and networth at mid game time
    for i, k in zip(range(0, 5), range(5, 10)):
        rad_nw_mid = r_obj['data']['match']['players'][i]['stats']['networthPerMinute'][midgame_time]
        radiant_tuple.append(tuple([r_obj['data']['match']['players'][i]['heroId'], r_obj['data']['match']
                                    ['players'][i]['lane'], r_obj['data']['match']['players'][i]['roleBasic'], rad_nw_mid]))
        dire_nw_mid = r_obj['data']['match']['players'][k]['stats']['networthPerMinute'][midgame_time]
        dire_tuple.append(tuple([r_obj['data']['match']['players'][k]['heroId'], r_obj['data']['match']
                                 ['players'][k]['lane'], r_obj['data']['match']['players'][k]['roleBasic'], dire_nw_mid]))
    # Radiant assignment
    radiant_ids, radiant_safe, radiant_off, radiant_supp, radiant_roam = team_tuples(
        radiant_tuple, radiant_ids)  # creates tuple for every role in radiant
    radiant_ids, radiant_supp = assign_safe(
        radiant_ids, radiant_safe, radiant_supp)  # assigns the safelane in radiant_ids
    # assigns the offlane in radiant_ids
    radiant_ids = assign_off(radiant_ids, radiant_off)
    # assigns the supports in radiant_ids
    radiant_ids = assign_supp(radiant_ids, radiant_supp)
    if None in radiant_ids:  # missing details
        # assigns the missing role in radiant_ids
        radiant_ids = assign_missing(radiant_ids, radiant_roam)
        if radiant_ids is None:
            raise MissingDetails(
                "Radiant lineup issue.", f"IDS: {radiant_ids}, Safe: {radiant_safe}, Off: {radiant_off}, Supp: {radiant_supp}")
    clean['radiant_team']['heroes'] = radiant_ids
    # Dire assignment (follows the same rules as radiant)
    dire_ids, dire_safe, dire_off, dire_supp, dire_roam = team_tuples(
        dire_tuple, dire_ids)
    dire_ids, dire_supp = assign_safe(dire_ids, dire_safe, dire_supp)
    dire_ids = assign_off(dire_ids, dire_off)
    dire_ids = assign_supp(dire_ids, dire_supp)
    if None in dire_ids:  # missing details
        dire_ids = assign_missing(dire_ids, dire_roam)
        if dire_ids is None:
            raise MissingDetails(
                "Dire lineup issue.", f"IDS: {dire_ids}, Safe: {dire_safe}, Off: {dire_off}, Supp: {dire_supp}")
    clean['dire_team']['heroes'] = dire_ids
    return clean


def add_hints(r_obj, c_obj):
    """The dicitionary "c_obj" has its hints array populated. Hints are as follows:
    -Stratz flag
    -Match duration
    -Name of hero with highest net
    -Value of the richest hero's net
    -Team name with gold advantage post laning and value of the advantage
    -Team name with most damage dealt to heroes inc percentage increase relative to other team
    -Team name with most creeps slain inc percentage increase relative to other team
    -Number of trips back to fountain during laning phase per team
    -Amount of buybacks used per team
    -Team that had their mid tier 1 destroyed first

    :param r_obj: original response object
    :type r_obj: str
    :param c_obj: "cleaned up" response object
    :type c_obj: str
    :return: dictionary with the hints array populated
    :rtype: str
    """
    c_obj['hints'] = []
    # for loop for radiant and dire
    highest_net, richest_hero = 0, 0
    damage_radiant, damage_dire = 0, 0
    cs_radiant, cs_dire = 0, 0
    trips_radiant, trips_dire = 0, 0
    bb_radiant, bb_dire = 0, 0
    for i in range(0, 10):
        final_net = int(r_obj['data']['match']['players']
                        [i]['stats']['networthPerMinute'][-1])
        if final_net > highest_net:
            highest_net = final_net
            richest_hero = int(r_obj['data']['match']['players'][i]['heroId'])
    for i, k in zip(range(0, 5), range(5, 10)):
        damage_radiant += int(r_obj['data']['match']
                              ['players'][i]['stats']['heroDamageCount'])
        cs_radiant += int(r_obj['data']['match']
                          ['players'][i]['stats']['lastHitCount'])
        trips_radiant += sum(r_obj['data']['match']['players']
                             [i]['stats']['tripsFountainPerMinute'][:12])
        if r_obj['data']['match']['players'][i]['playbackData'] is not None:
            if None not in r_obj['data']['match']['players'][i]['playbackData']['buyBackEvents']:
                bb_radiant += len(r_obj['data']['match']['players']
                                  [i]['playbackData']['buyBackEvents'])
        damage_dire += int(r_obj['data']['match']
                           ['players'][k]['stats']['heroDamageCount'])
        cs_dire += int(r_obj['data']['match']['players']
                       [k]['stats']['lastHitCount'])
        trips_dire += sum(r_obj['data']['match']['players']
                          [k]['stats']['tripsFountainPerMinute'][:12])
        if r_obj['data']['match']['players'][k]['playbackData'] is not None:
            if None not in r_obj['data']['match']['players'][k]['playbackData']['buyBackEvents']:
                bb_dire += len(r_obj['data']['match']['players']
                               [k]['playbackData']['buyBackEvents'])
    # Stratz flag
    outcome_int = r_obj['data']['match']['analysisOutcome']
    if outcome_int is not None and outcome_int != 0:
        if outcome_int == 1:
            outcome_str = "stomp"
        elif outcome_int == 2:
            outcome_str = "comeback"
        elif outcome_int == 3:
            outcome_str = "close game"
        c_obj['hints'].append(
            f"STRATZ has flagged this match as a {outcome_str}.")
    # Match duration
    c_obj['hints'].append(f"The match duration was {c_obj['duration']}")
    # Name of hero with highest net & Value of the richest hero's net
    c_obj['hints'].append(
        f"{hdisplay(richest_hero)} had the highest networth at the end of the game.")
    c_obj['hints'].append(
        f"The highest networth on one hero was {highest_net} gold.")
    # Team name with gold advantage post laning and value of the advantage
    radiant_gold_adv = r_obj['data']['match']['stats']['radiantNetworthLeads']
    radiant_xp_adv = r_obj['data']['match']['stats']['radiantExperienceLeads']
    goldat12 = radiant_gold_adv[12]
    if goldat12 > 0:
        c_obj["hints"].append(
            f"Radiant had a {goldat12} gold advantage post laning phase.")
    else:
        c_obj["hints"].append(
            f"Dire had a {abs(goldat12)} gold advantage post laning phase.")
    # Team name with most damage dealt to heroes inc percentage increase relative to other team
    if damage_radiant > damage_dire:
        dmg_inc = roundup(percent_inc(damage_radiant, damage_dire))
        c_obj['hints'].append(
            f"The radiant team dealt {dmg_inc}% more hero damage than dire team.")
    else:
        dmg_inc = roundup(percent_inc(damage_dire, damage_radiant))
        c_obj['hints'].append(
            f"The dire team dealt {dmg_inc}% more hero damage than radiant team.")
    # Team name with most creeps slain inc percentage increase relative to other team
    if cs_radiant > cs_dire:
        cs_inc = roundup(percent_inc(cs_radiant, cs_dire))
        cs_inc = roundup(percent_inc(cs_radiant, cs_dire))
        c_obj['hints'].append(
            f"The radiant team farmed {cs_inc}% creeps than dire team.")
    else:
        cs_inc = roundup(percent_inc(cs_dire, cs_radiant))
        c_obj['hints'].append(
            f"The dire team farmed {cs_inc}% creeps than radiant team.")
    # Number of trips back to fountain during laning phase per team
    if trips_radiant == trips_dire:
        c_obj['hints'].append(
            f"Both teams had {trips_dire} trips back to fountain during the laning phase.")
    else:
        c_obj['hints'].append(
            f"Radiant had {trips_radiant} trips and Dire had {trips_dire} back to fountain during the laning phase.")
    # Amount of buybacks used per team
    if bb_radiant != 0 and bb_dire != 0:
        if bb_radiant == bb_dire:
            c_obj['hints'].append(
                f"Both teams used {bb_dire} buyback(s) during the match.")
        else:
            c_obj['hints'].append(
                f"Radiant used {bb_radiant} buyback(s) and Dire used {bb_dire} buyback(s) during the match.")
    # Team that had their mid tier 1 destroyed first
    if r_obj['data']['match']['playbackData'] is not None:
        if None not in r_obj['data']['match']['playbackData'].values():
            radiant_dead_towers, dire_dead_towers = 0, 0
            gamedur_seconds = r_obj['data']['match']['durationSeconds']
            radiant_mid_t1_time, dire_mid_t1_time = gamedur_seconds, gamedur_seconds
            for i in r_obj['data']['match']['playbackData']['towerDeathEvents']:
                if i['radiant'] - radiant_dead_towers == 2:
                    radiant_mid_t1_time = i['time']
                else:
                    radiant_dead_towers = i['radiant']
                if i['dire'] - dire_dead_towers == 2:
                    dire_mid_t1_time = i['time']
                else:
                    dire_dead_towers = i['dire']
                if radiant_mid_t1_time != gamedur_seconds and dire_mid_t1_time != gamedur_seconds:
                    break
            if radiant_mid_t1_time == dire_mid_t1_time:
                pass
            elif radiant_mid_t1_time > dire_mid_t1_time:
                c_obj['hints'].append(
                    f"Dire's mid tier 1 tower was destroyed earlier than radiants.")
            else:
                c_obj['hints'].append(
                    f"Radiant's mid tier 1 tower was destroyed earlier than dires.")
    return c_obj


def league_query(league_id, skip=0):
    """Consumes Stratz GraphQL API in order to return match-ids and relevant information tied to the league_id arg.

    :param league_id: id of the dota league
    :type league_id: int
    :param skip: number of matches to skip, defaults to 0
    :type skip: int, optional
    :return: dictionary containing relevant information of the league
    :rtype: str
    """
    url = 'https://api.stratz.com/graphql'
    query = """
  query league_matches {
    league(id: %s) {
      displayName
      matches(request: {skip: %s, take: 100, isParsed: true}) {
        id
        analysisOutcome
        durationSeconds
        didRadiantWin
        stats {
          radiantNetworthLeads
          radiantExperienceLeads
          direKills
          radiantKills
        }
        players {
          imp
        }
      }
    }
  }
  """ % (json.dumps(league_id), skip)
    try:
        r = requests.post(url=url, json={'query': query}, headers={
                          "Authorization": f"Bearer {TOKEN}"})
        r_obj = r.json()
        return r_obj
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)


def analyse_league(r_obj):
    """Analyses the details of each match and adds the analysed match id to one of the three predefined lists.
    Matches with corrupted stats are skipped and the match id is discarded.

    :param r_obj: dictionary containing relevant information of the league
    :type r_obj: str
    :return: lists that contain match-ids at differing dificulty ratings
    :rtype: array
    """
    buffer_list, easy_ids, medium_ids, hard_ids = ([] for _ in range(4))
    for i in r_obj['data']['league']['matches']:
        match_id = i['id']
        # Checks for corrupted stats
        if i['stats']['radiantNetworthLeads'] is None or i['stats']['radiantExperienceLeads'] is None or i['stats']['radiantKills'] is None or i['stats']['direKills'] is None:
            continue
        # Duration in minutes rounded up
        duration_min = (-(-i['durationSeconds'] // 60))
        if duration_min == 0:
            continue
        # Radiant and dire kills
        radiant_kills, dire_kills = 0, 0
        for j in i['stats']['radiantKills']:
            radiant_kills += j
        for k in i['stats']['direKills']:
            dire_kills += k
        if dire_kills == 0 or radiant_kills == 0:
            continue
        kill_difference = radiant_kills - dire_kills
        # Team average IMP
        radiant_imp, dire_imp = 0, 0
        radiant_max, dire_max = 5, 5
        for j, l in zip(range(0, 5), range(5, 10)):
            if i['players'][j]['imp'] is not None:
                radiant_imp += i['players'][j]['imp']
            else:
                radiant_max -= 1
            if i['players'][l]['imp'] is not None:
                dire_imp += i['players'][l]['imp']
            else:
                dire_max -= 1
        if radiant_imp != 0:
            radiant_imp = int(radiant_imp / radiant_max)
        if dire_max != 0:
            dire_imp = int(dire_imp / dire_max)
        imp_difference = None
        if dire_max >= 4 and radiant_max >= 4:
            imp_difference = radiant_imp - dire_imp
        # Radiant graphs by minute
        nwlead = i['stats']['radiantNetworthLeads']
        xplead = i['stats']['radiantExperienceLeads']
        # networth from the penultimate minute mod the full game duration in minutes
        final_net = nwlead[duration_min - 3] // duration_min
        # nw_swing = final_net / nwlead[duration_min - 9]  # needs tweaking
        # xp_swing = xplead[duration_min - 3] / xplead[duration_min - 9]  # needs tweaking
        # Add match id to buffer list
        buffer_list.append(match_id)
        # Score logic
        score = 0
        if duration_min >= 60:
            score += 35
        elif duration_min >= 45:
            score += 15
        if (final_net <= -100 and i['didRadiantWin']) or (final_net >= 100 and not i['didRadiantWin']):
            score += 35
        if imp_difference is not None:
            if (imp_difference <= -15 and i['didRadiantWin']) or (imp_difference >= 15 and not i['didRadiantWin']):
                score += 20
        if (kill_difference < 0 and i['didRadiantWin']) or (kill_difference > 0 and not i['didRadiantWin']):
            score += 35
        elif -6 <= kill_difference <= 6:
            score += 15
        if i['analysisOutcome'] == 2 or i['analysisOutcome'] == 3:
            score += 15
        # sorting to lists based on score
        if score >= 55:
            buffer_list.remove(match_id)
            hard_ids.append(match_id)
        elif score >= 30:
            buffer_list.remove(match_id)
            medium_ids.append(match_id)
        print(match_id, score, kill_difference, i['didRadiantWin'])
    easy_ids = buffer_list  # remaining match ids are flagged as easy
    return easy_ids, medium_ids, hard_ids


def check_id(league_id):
    """Checks if id exists in json file and returns index if found

    :param league_id: id of the dota 2 league
    :type league_id: int
    :return: index of the league in leagues json array
    :rtype: int
    """
    with open('json/leagues.json', 'r') as jfile:
        data = jfile.read()
    obj = json.loads(data)
    for v, i in enumerate(obj['leagues']):
        if i['id'] == league_id:
            return v


def id_prompt():
    """Prompts the user to input valid league id & if the list should be updated or reset.

    :raises ValueError: League ID doesn't exist in the leagues json array
    :raises ValueError: Input did not match requirement
    :return: league id, index of league in leagues json array, an identifier to distinguish between operations
    :rtype: int
    """
    while True:
        try:
            league = int(input("Enter league id to create 3 lists:"))
            index = check_id(league)
            if index is None:
                raise ValueError
            k = int(input("Updating/Restting? (1/2):"))
            if k == 1 or k == 2:
                return league, index, k
            else:
                raise ValueError
        except ValueError:
            print("Invalid input.")


def add_lists(index, k, easy_ids, medium_ids, hard_ids):
    """The json file is changed depedning on the value of k

    :param index: index of the league in leagues json array
    :type index: int
    :param k: an identifier to distinguish between operations
    :type k: int
    :param easy_ids: List of match-ids flagged as easy
    :type easy_ids: int
    :param medium_ids: List of match-ids flagged as medium
    :type medium_ids: int
    :param hard_ids: List of match-ids flagged as hard
    :type hard_ids: int
    """
    with open('json/leagues.json', 'r') as jfile:
        data = jfile.read()
    obj = json.loads(data)
    league = obj['leagues'][index]
    if k == 1:
        league['ids']['easy'] = list(set(league['ids']['easy']) | set(easy_ids))
        league['ids']['medium'] = list(set(league['ids']['medium']) | set(medium_ids))
        league['ids']['hard'] = list(set(league['ids']['hard']) | set(hard_ids))
    elif k == 2:
        league['ids']['easy'] = easy_ids
        league['ids']['medium'] = medium_ids
        league['ids']['hard'] = hard_ids
    with open('json/leagues.json', 'w') as out:
        json.dump(obj, out)


def local_query():
    """Test local query sampled from stratz graphql

    :return: json object
    :rtype: str
    """
    with open('json/samplegql.json', 'r') as sample:
        data = sample.read()
    obj = json.loads(data)
    return obj


if __name__ == '__main__':
    import time
    start = time.time()
    try:
        r_obj, full = match_query(5467338855, 1)
        r_obj = isParsed(r_obj, full)
        c_obj = clean_obj(r_obj)
        if full:
            c_obj = add_hints(r_obj, c_obj)
        print(c_obj)
        end = time.time()
        print(f"Took {(end-start)*1000}ms")
    except MissingDetails as e:
        print(str(e))
        print(f"Match id: {e.payload}")

        '''
    # add match_ids to league lists
    l, index, k = id_prompt()
    r_obj = league_query(l)
    easy_ids, medium_ids, hard_ids = analyse_league(r_obj)
    add_lists(index, k, easy_ids, medium_ids, hard_ids)
        '''
