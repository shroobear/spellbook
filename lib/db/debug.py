#!/usr/bin/env python3

import ipdb
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Spell, User, Character, Spellbook

engine = create_engine("sqlite:///spell.db")
Session = sessionmaker(bind=engine)
session = Session()

# from seed import populate_spells, populate_user, populate_character, assign_spells

ipdb.set_trace()
