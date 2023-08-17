from models import Spell, User, Character, Spellbook
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from faker import Faker
import fantasynames as names
import random
from alive_progress import alive_bar, alive_it

engine = create_engine("sqlite:///spell.db")
Session = sessionmaker(bind=engine)
session = Session()

fake = Faker()

import requests

response = requests.get("https://www.dnd5eapi.co/api/spells/")
json_data = response.json()
spells = json_data['results']

def clear_table(table_class):
    session.query(table_class).delete()
    session.commit()

def clear_all():
    clear_table(User)
    clear_table(Spell)
    clear_table(Character)
    clear_table(Spellbook)

def populate_spells():
    print("Seeding Spells 🪄\n")
    for entry in alive_it(spells):
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
                spell_damage = list(damage_at_slot_level.values())[0]
            elif 'damage_at_character_level' in spell_data['damage']:
                damage_at_character_level = spell_data['damage']['damage_at_character_level']
                spell_damage = list(damage_at_character_level.values())[0]
        else:
            damage_type = None
            spell_damage = None
        if spell_data.get('heal_at_slot_level'):
            healing = list(spell_data['heal_at_slot_level'].values())[0]
        else:
            healing = None
        
        class_list = ", ".join([cls['name'] for cls in spell_data['classes']])

        
        school = spell_data['school']['name']        

        new_spell = Spell(
            name = spell_data['name'],
            description = '\n\n'.join(spell_data['desc']),
            casting_level = int(spell_data['level']),
            higher_level = '\n'.join(spell_data['higher_level']),
            components = ', '.join(spell_data['components']),
            range = spell_data['range'],
            material = material,
            ritual = int(spell_data['ritual']),
            duration = spell_data['duration'],
            concentration = int(spell_data['concentration']),
            casting_time = spell_data['casting_time'],
            school = school,
            damage_type = damage_type,
            damage = spell_damage,
            healing = healing,
            classes = class_list
        )
        session.add(new_spell)
    session.commit()
    print("\nSpells seeded successfully 🌱\n")


def populate_user():
    print("Seeding users 👥\n")

    Faker.seed(0)
    with alive_bar(50) as bar:
        for i in range(50):
            user = fake.simple_profile()
            new_user = User(
                username = user['username'],
                first_name = fake.first_name(),
                last_name = fake.last_name(),
            )
            bar()
            session.add(new_user)
        session.commit()
    print("\nUsers seeded successfully 🌱\n")

def populate_character():
    print("Seeding characters 🧌\n")
    classes = ["Barbarian",
        "Bard", 
        "Cleric", 
        "Druid", 
        "Fighter", 
        "Monk", 
        "Paladin",
        "Ranger",
        "Rogue",
        "Sorcerer", 
        "Warlock", 
        "Wizard"
    ]

    Faker.seed(0)
    with alive_bar(125) as bar:
        for i in range(125):
            new_character = Character(
                name = names.human(),
                level = random.randint(1, 20),
                user_id = random.randint(1, 50),
                character_class = random.choice(classes)
            )
            bar()
            session.add(new_character)

        session.commit()
    print("\nCharacters seeded successfully 🌱\n")

def assign_spells():
    print("Learning Spells 📖\n")
    spell_count = session.query(Spell).count()
    character_count = session.query(Character).count()
    with alive_bar(1000) as bar:
        for i in range(1000):
            random_spell = random.randint(1, spell_count)
            random_character = random.randint(1, character_count)

            learned_spell = Spellbook(
                character_id = random_character,
                spell_id = random_spell
            )
            bar()
            session.add(learned_spell)
        
        session.commit()
    print("\nSpellbooks seeded successfully 🌱\n")

def seed_all():
    clear_all()
    populate_spells()
    populate_user()
    populate_character()
    assign_spells()

seed_all()