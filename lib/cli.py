#!/usr/bin/env python3
import click
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

class Prompt():
    def ask(question):
        value = input(question)
        return value
    
    def yes_or_no(question):
        value = input(question + " y/n")

def main():
    clear_screen(10)
    spellbook_banner()
    clear_screen(3)
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
    pass

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
    click.echo(f"New user added successfully. Welcome, {first_name}!")
    home()

def home():
    pass

def quit():
    pass


if __name__ == "__main__":
    main()