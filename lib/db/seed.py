from models import Spell, User, Character
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from faker import Faker

engine = create_engine("sqlite:///spell.db")
Session = sessionmaker(bind=engine)
session = Session()

fake = Faker()

import requests
import json

response = requests.get("https://www.dnd5eapi.co/api/spells/")
json_data = response.json()
spells = json_data['results']

def clear_table(table_class):
    session.query(table_class).delete()
    session.commit()

def populate_spells():
    clear_table(Spell)

    for entry in spells:
        r = requests.get(f"http://www.dnd5eapi.co{entry['url']}")
        spell_data = r.json()

        material = spell_data.get('material', None)
        # damage_type = spell_data['damage']['damage_type']['name']
        school = spell_data['school']['name']

        # import ipdb; ipdb.set_trace()
        new_spell = Spell(
            name = spell_data['name'],
            description = '/n'.join(spell_data['desc']),
            casting_level = int(spell_data['level']),
            higher_level = spell_data['higher_level'],
            components = ', '.join(spell_data['components']),
            range = spell_data['range'],
            material = material,
            ritual = int(spell_data['ritual']),
            duration = spell_data['duration'],
            concentration = int(spell_data['concentration']),
            casting_time = spell_data['casting_time'],
            # damage_type = damage_type,
            school = school
        )
        session.add(new_spell)

    session.commit()


def populate_user():
    clear_table(User)

    Faker.seed(0)
    for _ in range(10):
        user = fake.simple_profile()
        new_user = User(
            username = user['username'],
            first_name = fake.first_name(),
            last_name = fake.last_name(),
        )
        session.add(new_user)
    session.commit()

    

# populate_spells()
populate_user()

import ipdb; ipdb.set_trace()