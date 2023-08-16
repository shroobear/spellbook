#!/usr/bin/env python3
import time
from art import *
# from filter import Filter
from prompt import Prompt
from helpers import *
from banners import Banner
from db.models import Spell, User, Character, Spellbook
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, delete
from prettycli import color

engine = create_engine("sqlite:///db/spell.db")
Session = sessionmaker(bind=engine)
session = Session()

# Global
current_user = None
current_character = None
character_classes = [
    "Barbarian",
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
    "Wizard",
]

# Notes: Break into appropriate classes
# Separate session into its own file
# Terminal menu in prompt class


def main():
    Banner.spellbook()
    global current_user
    current_user = None
    options = {
        "Login": login,
        "Create New User": new_user,
        "View Spells": view_all_spells,
        "Filter Spells": filter_spells,
        "Quit": quit,
    }
    Prompt.dict_menu(options)


def login():
    value = input("Please enter username: ")
    validation = session.query(User).filter(User.username.like(f"%{value}%")).first()
    if validation == None:
        val = input(
            f"User '{value}' not found. Would you like to create a new user? y/n: "
        )
        if val in ["Y", "y", "yes", "Yes"]:
            new_user()
        else:
            main()
    elif validation.username == value:
        print(f"Welcome back, {validation.first_name}!")
        global current_user
        current_user = session.query(User).filter(User.username == validation.username)[
            0
        ]
        time.sleep(1)
        character_select()


def new_user():
    first_name = Prompt.ask("Please enter first name: ")
    last_name = Prompt.ask("Please enter last name: ")
    username = Prompt.ask("Please create a username: ")
    new_user = User(
        username=username,
        first_name=first_name,
        last_name=last_name,
    )
    session.add(new_user)
    session.commit()
    global current_user
    current_user = session.query(User).filter(User.username == new_user.username)[0]
    print(f"New user added successfully. Welcome, {first_name}!")
    time.sleep(1)
    character_select()


def character_select():
    Banner.spellbook()
    print("Characters:\n")
    characters = []
    for character in current_user.characters:
        characters.append(character.name)
    choices = characters + ["", "Logout", "Create New Character", "Quit"]
    selection = Prompt.menu(choices)
    if selection == "Logout":
        main()
    elif selection == "Create New Character":
        create_character()
    elif selection == "Quit":
        quit()
    else:
        open_character(selection)


def open_character(character_name):
    global current_character
    current_character = (
        session.query(Character).filter(Character.name == character_name).first()
    )
    banner_name = "\n".join(character_name.split())
    Banner.generator(banner_name, 255, 105, 180)
    print(
        f"Character Level: {current_character.level}\n"
        f"Character Class: {current_character.character_class}\n"
        "Spells:"
    )
    for spellbook in current_character.spells:
        spell = spellbook.spell
        if spell.damage:
            print(color(spell.name).rgb_fg(210, 4, 45))
        elif spell.healing:
            print(color(spell.name).rgb_fg(80, 200, 120))
        else:
            print(color(spell.name).rgb_fg(0, 255, 255))

    options = {
        "Edit Spells": edit_spells,
        "View a Learned Spell": character_spells_prompt,
        "View Master Spell List": view_all_spells,
        "Filter Spells": filter_spells,
        "Return to Character Select": character_select,
        "Delete Character": delete_character,
        "Quit": quit,
        }
    Prompt.dict_menu(options)

def character_spells_prompt():
    spells = get_character_spells()
    print("\nPlease select a spell: \n")
    selection = Prompt.menu(spells)
    view_spell(selection)


def delete_character():
    confirmation = input(f"Are you sure you'd like to delete {current_character.name} and all their data? y/n: ")
    if confirmation in ["y", "Y", "yes", "Yes", "YES"]:
        character = session.query(Character).filter(Character.id == current_character.id).first()
        session.delete(character)
        session.commit()
        character_select()
    else:
        open_character(current_character.name)

def create_character():
    print("New Character:")
    name = Prompt.ask("Please enter a character name: ")
    if name == None or len(name) > 45:
        print("Please enter a valid name")
        time.sleep(1)
        create_character()
    level = Prompt.ask("Please enter a character level 1-20: ")
    if int(level) > 20:
        print("Please enter a valid level 1-20")
        time.sleep(1)
        create_character()

    selection = Prompt.menu(character_classes)

    new_character = Character(
        name=name, level=level, character_class=selection, user_id=current_user.id
    )
    session.add(new_character)
    session.commit()
    open_character(new_character.name)


def view_all_spells():
    spells = session.query(Spell).all()
    selected_spell = spell_index(spells)
    validate_spell_selection(selected_spell, view_all_spells)

def spell_index(spells):
    for spell in spells:
        if current_character:
            if spell.name in get_character_spells():
                print(color(spell.name).rgb_fg(0, 255, 255))
            if spell.damage:
                print(color(spell.name).rgb_fg(210, 4, 45))
            elif spell.healing:
                print(color(spell.name).rgb_fg(80, 200, 120))
            else:
                print(spell.name)
        elif current_character == None:
            if spell.damage:
                print(color(spell.name).rgb_fg(210, 4, 45))
            elif spell.healing:
                print(color(spell.name).rgb_fg(80, 200, 120))
            else:
                print(spell.name)
    print("Color Key:", color("[Attack Spells]").rgb_fg(210, 4, 45), color("[Healing Spells]").rgb_fg(80, 200, 120), color("[Learned Spells]").rgb_fg(0, 255, 255))
    spell_selection = Prompt.ask("\nPlease enter a spell name to view it:\n")
    return spell_selection

def validate_spell_selection(selected_spell, return_func):
    validation = (
        session.query(Spell).filter(Spell.name.like(f"%{selected_spell}%")).first()
    )
    if validation == None:
        clear_screen(40)
        print(f"'{selected_spell}' not found.")
        time.sleep(0.5)
        return_func()
    elif validation.name.lower() == selected_spell.lower():
        clear_screen(30)
        input(f"You selected {validation.name}. Press Enter to confirm.")
        clear_screen(30)
        view_spell(validation.name)

def view_spell(spell):
    query = session.query(Spell).filter(Spell.name == spell).first()
    Banner.generator(query.name)
    print(query)
    clear_screen(2)
    if current_character:
        if spell in get_character_spells():
            options= {
                "Forget Spell": lambda: remove_spell(spell),
                "Return to Spell List": view_all_spells,
                "Return to Character": lambda: open_character(current_character.name),
                "Quit": quit
            }
        else:
            options = {
                "Learn Spell": lambda: learn_spell(query),
                "Return to Spell List": view_all_spells,
                "Return to Character": lambda: open_character(current_character.name),
                "Quit": quit
            }
    else: options = {
        "Return to Spell List": view_all_spells,
        "Home": main,
        "Quit": quit
    }
    Prompt.dict_menu(options)


def learn_spell(spell):
    learned_spell = Spellbook(
        spell_id=spell.id,
        character_id=current_character.id,
    )
    session.add(learned_spell)
    session.commit()
    print("Spell Learned successfully 🧙‍♂️")
    time.sleep(1)
    open_character(current_character.name)

def edit_spells():
    print("Select a spell to remove: \n")
    options = []
    for spellbook in current_character.spells:
        options.append(spellbook.spell.name)
    options.append("Return")
    selection = Prompt.menu(options)
    if selection == "Return":
        open_character(current_character.name)
    else:
        remove_spell(selection)


def get_character_spells():
    list = []
    for spell_obj in current_character.spells:
        list.append(spell_obj.spell.name)
    return list


def remove_spell(spell_selection):
    value = str(
        input(
            f"You've selected {spell_selection}. Are you sure you'd like to remove this spell? y/n: "
        )
    )
    if value in ["y", "Y", "Yes", "yes", "YES"]:
        spell_id = session.query(Spell).filter(Spell.name == spell_selection).first().id
        char_id = current_character.id
        spellbook_object = (
            session.query(Spellbook)
            .filter(Spellbook.spell_id == spell_id, Spellbook.character_id == char_id)
            .first()
        )
        session.delete(spellbook_object)
        session.commit()

        print(f"{spell_selection} unlearned 🤯")
        time.sleep(1)
        open_character(current_character.name)
    elif value in ["N", "n", "no", "No", "NO"]:
        edit_spells()
    else:
        print("Command not recognized")
        time.sleep(1)
        open_character(current_character.name)


def filter_spells():
    options = {
        "Sort Spells by Level": filter_spells_by_level,
        "Attack Spells": filter_attack_spells,
        "Healing Spells": filter_healing_spells,
        "Sort Spells by School": filter_spells_by_school,
        "Sort Spells by Class": filter_spells_by_class,
    }
    Prompt.dict_menu(options)


def filter_spells_by_level():
    # debug()
    print("Please select a casting level:")
    levels = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    selection = Prompt.menu(levels)
    spell_list = session.query(Spell).filter(Spell.casting_level == selection)
    spell_selection = spell_index(spell_list)
    validate_spell_selection(spell_selection, filter_spells_by_level)


def filter_attack_spells():
    attack_spells = session.query(Spell).filter(Spell.damage != None)
    print("Attack Spells:")
    spell_selection = spell_index(attack_spells)
    validate_spell_selection(spell_selection, filter_attack_spells)


def filter_healing_spells():
    healing_spells = session.query(Spell).filter(Spell.healing != None)
    spell_selection = spell_index(healing_spells)
    validate_spell_selection(spell_selection, filter_healing_spells)


def filter_spells_by_school():
    print("Please select a school:")
    schools = [
        "Conjuration",
        "Evocation",
        "Illusion",
        "Necromancy",
        "Enchantment",
        "Transmutation",
        "Abjuration",
        "Divination",
    ]
    selection = Prompt.menu(schools)
    school_spells = session.query(Spell).filter(Spell.school == selection)
    spell_selection = spell_index(school_spells)
    validate_spell_selection(spell_selection, filter_spells_by_school)


def filter_spells_by_class():
    print("Please select a class:")
    class_selection = Prompt.menu(character_classes)
    class_spells = session.query(Spell).filter(
        Spell.classes.like(f"%{class_selection}%")
    )
    spell_selection = spell_index(class_spells)
    validate_spell_selection(spell_selection, filter_spells_by_class)




def quit():
    Banner.goodbye()
    exit()


def debug():
    import ipdb

    ipdb.set_trace()


if __name__ == "__main__":
    main()
