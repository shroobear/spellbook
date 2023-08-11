from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Spell(Base):
    __tablename__ = 'spell'

    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    casting_level = Column(Integer, nullable=False)
    components = Column(String)
    range = Column(String)
    material = Column(String)
    ritual = Column(Integer)
    duration = Column(String)
    concentration = Column(Integer)
    casting_time = Column(String)
    damage_type = Column(String)
    school = Column(String)

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)

    username = Column(String, nullable=False, unique=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)

class Character(Base):
    __tablename__ = 'character'

    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False)
    level = Column(Integer)
    user_id = relationship('User', backref='character')