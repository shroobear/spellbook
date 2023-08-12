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
    print("Seeding Spells 🪄")

    for entry in spells:
        r = requests.get(f"http://www.dnd5eapi.co{entry['url']}")
        spell_data = r.json()

        material = spell_data.get('material', None)
        if spell_data.get('damage'):
            if 'damage_type' in spell_data['damage']:
                damage_type = spell_data['damage']['damage_type']['name']
            else:
                damage_type = "TBD"
            if 'damage_at_slot_level' in spell_data['damage']:
                damage_at_slot_level = spell_data['damage']['damage_at_slot_level']
                first_dice_value = list(damage_at_slot_level.values())[0]
                damage = first_dice_value
            else:
                damage = None
        else:
            damage_type = None
        if spell_data.get('heal_at_slot_level'):
            heal_at_slot_level = list(spell_data['heal_at_slot_level'].values())
            healing = heal_at_slot_level[0]
        else:
            healing = None
        # import ipdb; ipdb.set_trace()

        
        school = spell_data['school']['name']        

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
            # damage is a stretch goal, there's a lot of nested JSON to navigate
            school = school,
            damage_type = damage_type,
            damage = damage,
            healing = healing
        )
        print(new_spell.healing)
        session.add(new_spell)
        session.commit()
    print(session.query(Spell).count(), " Spells seeded successfully 🌱")


def populate_user():
    clear_table(User)
    print("Seeding users 👥")

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
    print("Users seeded successfully 🌱")

def populate_character():
    clear_table(Character)
    print("Seeding characters 🧌")

    Faker.seed(0)
    for _ in range(25):
        new_character = Character(
            name = names.human(),
            level = random.randint(1, 20),
            user_id = random.randint(1, 10)
        )
        session.add(new_character)

    session.commit()
    print("Characters seeded successfully 🌱")

def assign_spells():
    clear_table(Spellbook)
    print("Learning Spells 📖")
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
    print("Spellbooks seeded successfully 🌱")

populate_spells()
populate_user()
populate_character()
assign_spells()