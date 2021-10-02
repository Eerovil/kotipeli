import json
from random import choice

from flask import Flask, request

app = Flask(__name__)

CODES = [
    'kissa',
    'koira',
    'ukki',
    'mummo',
    'joulupukki',
    'murkku',
    'banaani',
]

LOCATIONS = {
    '1': 'Valtterin huoneesta',
    '2': 'Einarin huoneesta',
}

LOCATIONS_TO = {
    '1': 'Valtterin huoneeseen',
    '2': 'Einarin huoneeseen',
}

@app.route("/")
def endpoint():
    location = request.args.get('location', '')
    code = request.args.get('code', '')
    if code and location:
        db = db_read()
        mission = db.get('mission', {})

        if not mission:
            db['mission'] = generate_mission()
            mission = db['mission']
            db_write(db)

        if code != mission.get('code')or location != mission.get('location'):
            return mission_text()


        db[location].append(code)
        db[location] = list(set(db[location]))
        for i in range(1, 3):
            if str(i) == location:
                continue
            db[str(i)] = list(filter(lambda x: x != code, db[str(i)]))
        db['mission'] = generate_mission()
        db_write(db)
        return "Kiitos, löysit kortin {}! {}!".format(code, mission_text())
    return "Terve"


def generate_mission():
    db = db_read()
    code = choice(CODES)
    possible_locations = []
    for key in LOCATIONS.keys():
        if code not in db[key]:
            possible_locations.append(key)

    location = choice(possible_locations)
    return {
        'location': location,
        'code': code,
    }

def mission_text():
    db = db_read()
    mission = db.get('mission', {})
    location = mission.get('location')
    code = mission.get('code')
    for i in range(1, 3):
        if code in db[str(i)]:
            return 'Hae {} {} ja vie se {}'.format(
                code, LOCATIONS[str(i)], LOCATIONS_TO[location]
            )
    return 'Hae {} ja vie se {}'.format(
        code, LOCATIONS_TO[location]
    ) 

def db_read():
    db = None
    try:
        with open('db.json', 'r') as f:
            db = json.load(f)
    except Exception as err:
        print('db init: {}'.format(err))
        db = init_db()
    return db


def db_write(full_db):
    with open('db.json', 'w') as f:
        json.dump(full_db, f)
    return


def init_db():
    db = {
      '1': [],
      '2': [],
      '3': [],
      'mission': {}
    }
    with open('db.json', 'w') as f:
        json.dump(db, f)
    return db

