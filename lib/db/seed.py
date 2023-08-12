from models import Spell, User, Character, Spellbook
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from faker import Faker
import fantasynames as names
import random

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
        casting_level = int(spell_data['level'])
        

        # import ipdb; ipdb.set_trace()
        print("Seeding Spells 🪄")
        new_spell = Spell(
            name = spell_data['name'],
            description = '/n'.join(spell_data['desc']),
            casting_level = int(spell_data['level']),
            higher_level = '/n'.join(spell_data['higher_level']),
            components = ', '.join(spell_data['components']),
            range = spell_data['range'],
            material = material,
            ritual = int(spell_data['ritual']),
            duration = spell_data['duration'],
            concentration = int(spell_data['concentration']),
            casting_time = spell_data['casting_time'],
            # damage_type = damage_type,
            # damage is a stretch goal, there's a lot of nested JSON to navigate
            school = school
        )
        print(new_spell.name, new_spell.casting_level)
        session.add(new_spell)
        session.commit()
    print(session.query(Spell)[-1], " Spells seeded successfully")


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

def populate_character():
    clear_table(Character)

    Faker.seed(0)
    for _ in range(25):
        new_character = Character(
            name = names.human(),
            level = random.randint(1, 20),
            user_id = random.randint(1, 10)
        )
        session.add(new_character)

    session.commit()

def assign_spells():
    # clear_table(Spellbook)
    spell_count = session.query(Spell).count()
    character_count = session.query(Character).count()

    for _ in range(200):
        random_spell = random.randint(1, spell_count)
        random_character = random.randint(1, character_count)

        learned_spell = Spellbook(
            character_id = random_character,
            spell_id = random_spell
        )
        session.add(learned_spell)
    
    session.commit()


import ipdb; ipdb.set_trace()
# populate_spells()
# populate_user()
# populate_character()
# assign_spells()
