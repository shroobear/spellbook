from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine("sqlite:///spell.db")
Session = sessionmaker(bind=engine)
session = Session()