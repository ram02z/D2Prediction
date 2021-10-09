import os
from flask import Flask, jsonify, make_response, render_template, request
from flask_cors import CORS
from werkzeug.exceptions import default_exceptions, abort
import rest
import graphql
import json
import random
import re

os.chdir(os.path.dirname(__file__))
app = Flask(__name__)
app.config.from_object('config.DevConfig')
CORS(app, resources={r'/*': {'origins': '*'}})


def ux_heroes(hero_list):
    with open('json/heroes.json', 'r') as heroes:
        data = heroes.read()
    obj = json.loads(data)
    for index, hero in enumerate(hero_list):
        for j in obj['data']['constants']['heroes']:
            if hero == j['id']:
                hero_list[index] = [j['displayName'], j['image_url']]
    return hero_list


# Error handling
def _handle_http_exception(e):
    return jsonify(error=True, data={
        'message': str(e.description),
        'payload': e.code})


for code in default_exceptions:
    app.errorhandler(code)(_handle_http_exception)


@app.route('/api/randomMatches', methods=['GET'])
def randomMatches():
    try:
        if 'test' in request.args:
            with open('json/samplerandpro.json', 'r') as sample:
                data = sample.read()
            obj = json.loads(data)
            matches, patch = obj['data']['ids'], obj['data']['patch']
        else:
            patch = request.args.get('patch')
            if patch is not None and re.match(r'^\d{1}(\.\d{2})?$', patch):  # matches patch numbers in the following format: 7.20
                matches = rest.random_matches(patch)
            else:
                matches = rest.random_matches()
        return jsonify(error=False, data={
            'count': len(matches),
            'patch': patch,
            'ids': matches
        })
    except graphql.MissingDetails as e:
        return jsonify(error=True, data={
            'message': str(e),
            'payload': str(e.payload),
            'headers': str(e.headers)
        })


@app.route('/api/match/<int:match_id>', methods=['GET'])
def match(match_id):
    try:
        if request.args['full'] == 'true':
            r_obj, full = graphql.match_query(match_id, 1)
        else:
            r_obj, full = graphql.match_query(match_id)
        r_obj = graphql.isParsed(r_obj, full)
        c_obj = graphql.clean_obj(r_obj)
        if full:
            c_obj = graphql.add_hints(r_obj, c_obj)
        c_obj['dire_team']['heroes'] = ux_heroes(c_obj['dire_team']['heroes'])
        c_obj['radiant_team']['heroes'] = ux_heroes(c_obj['radiant_team']['heroes'])
        return jsonify(error=False, data=c_obj)
    except graphql.MissingDetails as e:
        return jsonify(error=True, data={
            'message': str(e),
            'payload': str(e.payload),
            'headers': str(e.headers)
        })


@app.route('/api/filteredLive', methods=['GET'])
def filteredLive():
    try:
        if 'test' not in request.args:
            obj = rest.filter_live()
        else:
            with open('json/samplelive.json', 'r') as sample:
                data = sample.read()
            obj = json.loads(data)
        if 'ux' in request.args:
            for i in obj:
                i['dire_team']['heroes'] = ux_heroes(i['dire_team']['heroes'])
                i['radiant_team']['heroes'] = ux_heroes(i['radiant_team']['heroes'])
        return jsonify(error=False, data=obj)
    except graphql.MissingDetails as e:
        return jsonify(error=True, data={
            'message': str(e),
            'payload': str(e.payload),
            'headers': str(e.headers)
        })


@app.route('/api/matchDetail/<int:match_id>', methods=['GET'])
def matchDetail(match_id):
    try:
        obj = rest.get_match(match_id)
        if 'winner' in request.args:
            obj = {'id': match_id, 'radiant_win': obj['result']['radiant_win']}
        return jsonify(error=False, data=obj)
    except graphql.MissingDetails as e:
        return jsonify(error=True, data={
            'message': str(e),
            'payload': str(e.payload),
            'headers': str(e.headers)
        })


@app.route('/api/getHero/<int:hero_id>', methods=['GET'])
def getHero(hero_id):
    with open('json/heroes.json', 'r') as heroes:
        data = heroes.read()
    obj = json.loads(data)
    found = False
    for i in obj['data']['constants']['heroes']:
        if i['id'] == hero_id:
            found = True
            hero = {'id': i['id']}
            if not request.args:
                hero = i
            if 'displayName' in request.args:
                hero['displayName'] = i['displayName']
            if 'image_url' in request.args:
                hero['image_url'] = i['image_url']
            if 'roles' in request.args:
                hero['roles'] = i['roles']
            return jsonify(error=False, data=hero)
    if not found:
        return jsonify(error=True, data='Hero ID is invalid.')


@app.route('/api/getLeague/<int:league_id>', methods=['GET'])
def getLeague(league_id):
    with open('json/leagues.json', 'r') as leagues:
        data = leagues.read()
    obj = json.loads(data)
    found = False
    for i in obj['leagues']:
        if i['id'] == league_id:
            found = True
            league = {'id': i['id']}
            if not request.args:
                league = i
            if 'name' in request.args:
                league['name'] = i['name']
            if 'banner' in request.args:
                league['banner'] = i['banner']
            if 'version' in request.args:
                league['version'] = i['version']
            if 'matches' in request.args:
                league['black_list'] = i['black_list']
                match_arg = request.args['matches']
                if not match_arg:
                    league['easy_ids'] = i['easy_ids']
                    league['medium_ids'] = i['medium_ids']
                    league['hard_ids'] = i['hard_ids']
                else:
                    if "easy" in match_arg:
                        league['easy_ids'] = i['easy_ids']
                    if "medium" in match_arg:
                        league['medium_ids'] = i['medium_ids']
                    if "hard" in match_arg:
                        league['hard_ids'] = i['hard_ids']
            return jsonify(error=False, data=league)
    if not found:
        return jsonify(error=True, data='League ID is invalid.')


@app.route('/api/getLeagues', methods=['GET'])
def getLeagues():
    with open('json/leagues.json', 'r') as leagues:
        data = leagues.read()
    obj = json.loads(data)
    return jsonify(error=False, data=obj)


@app.route('/api/patchNames', methods=['GET'])
def patchNames():
    try:
        patch_res = rest.patch_odota()
        last = request.args.get('last', type=int)
        if type(last) == int and last < len(patch_res):
            patch_list = [d['name'] for d in patch_res if 'name' in d][-last:]
        else:
            patch_list = [d['name'] for d in patch_res if 'name' in d]
        return jsonify(error=False, data=patch_list)
    except graphql.MissingDetails as e:
        return jsonify(error=True, data={
            'message': str(e),
            'payload': str(e.payload),
            'headers': str(e.headers)
        })


if __name__ == "__main__":
    app.run()
