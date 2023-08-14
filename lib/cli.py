#!/usr/bin/env python3
import click
import time
from helpers import *
from banners import *
from db.models import Spell, User, Character, Spellbook
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, delete
from simple_term_menu import TerminalMenu

engine = create_engine("sqlite:///db/spell.db")
Session = sessionmaker(bind=engine)
session = Session()

current_user = None
current_character = None


class Prompt:
    def ask(question):
        value = input(question)
        return value

    def yes_or_no(question):
        value = input(question + " y/n: ")


def main():
    spellbook_banner()
    options = ["Login", "Create New User", "View Spells", "Quit"]
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    selection = options[menu_entry_index]
    if selection == "Login":
        login()
    elif selection == "Create New User":
        new_user()
    elif selection == "View Spells":
        view_spells()
    elif selection == "Quit":
        quit()


def login():
    value = input("Please enter username: ")
    validation = session.query(User).filter(User.username.like(f"%{value}%")).first()
    # import ipdb; ipdb.set_trace()
    if validation == None:
        spellbook_banner()
        print(f"User '{value}' not found")
        login()
    elif validation.username == value:
        print(f"Welcome back, {validation.first_name}!")
        global current_user
        current_user = session.query(User).filter(User.username == validation.username)[
            0
        ]
        time.sleep(1)
        character_select()

    # import ipdb; ipdb.set_trace()


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
    spellbook_banner()
    print("Characters:\n")
    options = []
    char_id = 1
    for character in current_user.characters:
        options.append(f"{character.name}")
        char_id += 1
    options.append("")
    options.append("Logout")
    options.append("Create New Character")
    terminal_menu = TerminalMenu(options, skip_empty_entries=True)
    menu_entry_index = terminal_menu.show()
    selection = options[menu_entry_index]
    if selection == "Logout":
        main()
    elif selection == "Create New Character":
        create_character()
    open_character(selection)


def open_character(character_name):
    global current_character
    current_character = (
        session.query(Character).filter(Character.name == character_name).first()
    )
    clear_screen(30)
    spellbook_banner()
    print(
        f"Character Name: {current_character.name}\n"
        f"Character Level: {current_character.level}\n"
        f"Character Class: {current_character.character_class}\n"
        "Spells:"
    )

    for spellbook in current_character.spells:
        spell = spellbook.spell
        print(spell.name)

    options = ["Remove Spells", "View Master Spell List", "Return", "Quit"]
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    selection = options[menu_entry_index]
    if selection == "Remove Spells":
        remove_spells()
    elif selection == "View Master Spell List":
        view_spells()
    elif selection == "Return":
        character_select()
    elif selection == "Quit":
        pass


def create_character():
    print("New Character:")
    name = Prompt.ask("Character Name: ")
    level = Prompt.ask("Character Level: ")
    classes = [
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
    terminal_menu = TerminalMenu(classes)
    menu_entry_index = terminal_menu.show()
    selection = classes[menu_entry_index]

    new_character = Character(
        name=name, level=level, character_class=selection, user_id=current_user.id
    )
    session.add(new_character)
    session.commit()
    open_character(new_character.name)

    # import ipdb; ipdb.set_trace()


def view_spells():
    spell_list = []
    spells = session.query(Spell).all()
    for spell in spells:
        spell_list.append(spell.name)
    print("\n".join(spell_list))
    selected_spell = Prompt.ask("Type a spell name to view it: ")
    validation = (
        session.query(Spell).filter(Spell.name.like(f"%{selected_spell}%")).first()
    )
    if validation == None:
        clear_screen(40)
        print(f"'{selected_spell}' not found.")
        time.sleep(0.5)
        view_spells()
    elif validation.name.lower() == selected_spell.lower():
        clear_screen(30)
        input(f"You selected {validation.name}. Press Enter to confirm.")
        clear_screen(30)
        view_spell(validation.name)


def view_spell(spell):
    query = session.query(Spell).filter(Spell.name == spell).first()
    print(query)
    if current_character:
        if spell in get_character_spells():
            options = [
                "Forget Spell",
                "Return to Spell List",
                "Return to Character",
                "Quit",
            ]
        else:
            options = [
                "Learn Spell",
                "Return to Spell List",
                "Return to Character",
                "Quit",
            ]

    else:
        options = ["Spell List", "Home", "Quit"]
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    selection = options[menu_entry_index]
    if selection == "Learn Spell":
        # import ipdb; ipdb.set_trace()
        learned_spell = Spellbook(
            spell_id=query.id,
            character_id=current_character.id,
        )
        session.add(learned_spell)
        session.commit()
        print("Spell Learned successfully 🧙‍♂️")
        time.sleep(1)
        open_character(current_character.name)
    elif selection == "Forget Spell":
        remove_spell(spell)
    elif selection == "Return to Spell List":
        view_spells()
    elif selection == "Return to Character":
        open_character(current_character.name)
    elif selection == "Quit":
        pass
    elif selection == "Spell List":
        view_spells()
    elif selection == "Logout":
        main()
    elif selection == "Quit":
        pass


def remove_spells():
    print("Select a spell to remove: \n")
    options = []
    for spellbook in current_character.spells:
        options.append(spellbook.spell.name)
    options.append("Return")
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    spell_selection = options[menu_entry_index]
    if spell_selection == "Return":
        open_character(current_character.name)
    else:
        remove_spell(spell_selection)


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
    if value == "y" or value == "Y":
        spell_id = session.query(Spell).filter(Spell.name == spell_selection).first().id
        char_id = current_character.id
        spellbook_object = (
            session.query(Spellbook)
            .filter(Spellbook.spell_id == spell_id, Spellbook.character_id == char_id)
            .first()
        )
        # import ipdb; ipdb.set_trace()
        session.delete(spellbook_object)
        session.commit()

        print(f"{spell_selection} unlearned 🤯")
        time.sleep(1)
        open_character(current_character.name)
    elif value == "n" or value == "N":
        remove_spells()
    else:
        print("Command not recognized")
        time.sleep(1)
        open_character(current_character.name)


def delete_character():
    pass


def quit():
    print("Goodbye!")
    exit()


if __name__ == "__main__":
    main()
