from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Spell(Base):
    __tablename__ = 'spell'

    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    casting_level = Column(Integer, nullable=False)
    higher_level = Column(String)
    components = Column(String)
    range = Column(String)
    material = Column(String)
    ritual = Column(Integer)
    duration = Column(String)
    concentration = Column(Integer)
    casting_time = Column(String)
    damage = Column(String)
    damage_type = Column(String)
    school = Column(String)
    healing = Column(String)
    classes = Column(String)
    spellbooks = relationship("Spellbook", back_populates='spell')
    

    def __repr__(self):
        return f"Spell id: {self.id} \n" \
            + f"Name: {self.name}\n" \
            + f"Description: \n{self.description}\n" \
            + f"Casting Level: {self.casting_level}\n" \
            + f"Higher Level: {self.higher_level}\n" \
            + f"Components: {self.components}\n" \
            + f"Range: {self.range}\n" \
            + f"Material: {self.material}\n" \
            + f"Ritual: {self.ritual}\n" \
            + f"Duration: {self.duration}\n" \
            + f"Concentration: {self.concentration}\n" \
            + f"Casting Time: {self.casting_time}\n" \
            + f"Damage: {self.damage} {self.damage_type} damage\n" \
            + f"Healing: {self.healing}\n" \
            + f"Classes: {self.classes}\n" \
            + f"School: {self.school}" \
               

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)

    username = Column(String, nullable=False, unique=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    characters = relationship('Character', backref = "user")

    def __repr__(self):
        return f"User(id={self.id} " \
            + f"Name: {self.first_name} {self.last_name})"

class Character(Base):
    __tablename__ = 'character'

    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False)
    level = Column(Integer)
    user_id = Column(Integer, ForeignKey('user.id'))
    spells = relationship('Spellbook', back_populates="character")

    __table_args__ = (
        CheckConstraint('level >= 1 AND level <= 20', name='check_character_level_range'),
    )

    def __repr__(self):
        return f"Character(id={self.id} " \
            + f"name: {self.name} " \
            + f"level: {self.level} "\
            + f"user_id: {self.user_id})"
    
class Spellbook(Base):
    __tablename__ = 'spellbook'

    id = Column(Integer, primary_key=True)

    character_id = Column(Integer, ForeignKey('character.id'))
    spell_id = Column(Integer, ForeignKey('spell.id'))

    character = relationship('Character', back_populates='spells')
    spell = relationship('Spell', back_populates = 'spellbooks')