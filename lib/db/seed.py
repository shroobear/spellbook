from models import Spell, User, Character
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine("sqlite:///spell.db")
Session = sessionmaker(bind=engine)
session = Session()

import requests
import json

response = requests.get("https://www.dnd5eapi.co/api/spells/")
json_data = response.json()
spells = json_data['results']

def populate_spells():
    for entry in spells:
        r = requests.get(f"http://www.dnd5eapi.co{entry['url']}")
        spell_data = r.json()
        print(spell_data)
        import ipdb; ipdb.set_trace()


populate_spells()