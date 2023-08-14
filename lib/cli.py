#!/usr/bin/env python3
import click
import time
from helpers import *
from banners import *
from db.models import Spell, User, Character, Spellbook
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from simple_term_menu import TerminalMenu

engine = create_engine("sqlite:///db/spell.db")
Session = sessionmaker(bind=engine)
session = Session()

current_user = None
current_character = None

class Prompt():
    def ask(question):
        value = input(question)
        return value
    
    def yes_or_no(question):
        value = input(question + " y/n")

def main():
    spellbook_banner()
    options = ["Login", "Create New User", "Quit"]
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    selection = options[menu_entry_index]
    if selection == "Login":
        login()
    elif selection == "Create New User":
        new_user()
    elif selection == "Quit":
        quit()

def login():
    value = input("Please enter username: ")
    validation = session.query(User).filter(User.username.like(f"%{value}%")).first()
    # import ipdb; ipdb.set_trace()
    if validation == None:
        clear_screen(40)
        print(f"User '{value}' not found")
        login()
    elif validation.username == value:
        print(f"Welcome back, {validation.first_name}!")
        global current_user
        current_user = session.query(User).filter(User.username == validation.username)[0]
        time.sleep(1)
        character_select()
    
    # import ipdb; ipdb.set_trace()

def new_user():
    first_name = Prompt.ask("Please enter first name: ")
    last_name = Prompt.ask("Please enter last name: ")
    username = Prompt.ask("Please create a username: ")
    new_user = User(
        username = username,
        first_name = first_name,
        last_name = last_name,
    )
    session.add(new_user)
    session.commit()
    global current_user
    current_user = session.query(User).filter(User.username == new_user.username)[0]
    print(f"New user added successfully. Welcome, {first_name}!")
    time.sleep(1)
    character_select()

def character_select():
    spellbook_banner()
    options = []
    char_id = 1
    for character in current_user.characters:
        options.append(f"{character.name}")
        char_id += 1
    options.append("Return")
    options.append("Create New Character")
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    selection = options[menu_entry_index]
    if selection == "Return":
        main()
    elif selection == "Create New Character":
        create_character()
    open_character(selection)

def open_character(selection):
    spellbook_banner()
    global current_character
    current_character = session.query(Character).filter(Character.name == selection).first()
    clear_screen(30)
    print(f"Character Name: {current_character.name}\n"
          f"Character Level: {current_character.level}\n"
          f"Character Class: {current_character.character_class}\n"
          "Spells:")
    
    for spellbook in current_character.spells:
        spell = spellbook.spell
        print(spell.name)

    input("Press Enter to go back to the character selection.")
    character_select()

def create_character():
    print("New Character:")
    name = Prompt.ask("Character Name: ")
    level = Prompt.ask("Character Level: ")
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
    terminal_menu = TerminalMenu(classes)
    menu_entry_index = terminal_menu.show()
    selection = classes[menu_entry_index]

    new_character = Character(
        name = name,
        level = level,
        character_class = selection,
        user_id = current_user.id
    )
    session.add(new_character)
    session.commit()
    open_character(new_character.name)
    
    # import ipdb; ipdb.set_trace()


def quit():
    print("Goodbye!")
    exit()


if __name__ == "__main__":
    main()