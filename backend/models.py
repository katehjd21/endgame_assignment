from peewee import *
from pg_db_connection import pg_db
import uuid


class BaseModel(Model):
    class Meta:
        database = pg_db

class Coin(BaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    name = CharField(unique=True, null = False)

class Duty(BaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    name = CharField(unique=True, null = False)

class Knowledge(BaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    name = CharField(unique=True)

class Skill(BaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    name = CharField(unique=True)

class Behaviour(BaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    name = CharField(unique=True)


# Junction Tables

class DutyCoin(BaseModel):
    duty = ForeignKeyField(Duty, backref="duty_coins")
    coin = ForeignKeyField(Coin, backref="coin_duties")
    class Meta:
        constraints = [SQL('UNIQUE(duty_id, coin_id)')]

class DutyKnowledge(BaseModel):
    duty = ForeignKeyField(Duty, backref="duty_knowledges")
    knowledge = ForeignKeyField(Knowledge, backref="knowledge_duties")
    class Meta:
        constraints = [SQL('UNIQUE(duty_id, knowledge_id)')]

class DutySkill(BaseModel):
    duty = ForeignKeyField(Duty, backref="duty_skills")
    skill = ForeignKeyField(Skill, backref="skill_duties")
    class Meta:
        constraints = [SQL('UNIQUE(duty_id, skill_id)')]

class DutyBehaviour(BaseModel):
    duty = ForeignKeyField(Duty, backref="duty_behaviours")
    behaviour = ForeignKeyField(Behaviour, backref="behaviour_duties")
    class Meta:
        constraints = [SQL('UNIQUE(duty_id, behaviour_id)')]

