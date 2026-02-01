from peewee import *
from backend.pg_db_connection import database
import uuid


class BaseModel(Model):
    class Meta:
        database = database

class Coin(BaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    name = CharField(unique=True, null = False)

class Duty(BaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    code = CharField(unique=True, null=False)
    name = CharField(unique=True, null = False)
    description = TextField(null=True)

class Knowledge(BaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    code = CharField(unique=True, null=False)
    name = CharField(unique=True)
    description = TextField(null=True)

class Skill(BaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    code = CharField(unique=True, null=False)
    name = CharField(unique=True)
    description = TextField(null=True)

class Behaviour(BaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    code = CharField(unique=True, null=False)
    name = CharField(unique=True)
    description = TextField(null=True)


# Junction Tables
class DutyCoin(BaseModel):
    duty = ForeignKeyField(Duty, backref="duty_coins", on_delete="CASCADE")
    coin = ForeignKeyField(Coin, backref="coin_duties", on_delete="CASCADE")
    class Meta:
        constraints = [SQL('UNIQUE(duty_id, coin_id)')]

class DutyKnowledge(BaseModel):
    duty = ForeignKeyField(Duty, backref="duty_knowledges", on_delete="CASCADE")
    knowledge = ForeignKeyField(Knowledge, backref="knowledge_duties", on_delete="CASCADE")
    class Meta:
        constraints = [SQL('UNIQUE(duty_id, knowledge_id)')]

class DutySkill(BaseModel):
    duty = ForeignKeyField(Duty, backref="duty_skills", on_delete="CASCADE")
    skill = ForeignKeyField(Skill, backref="skill_duties", on_delete="CASCADE")
    class Meta:
        constraints = [SQL('UNIQUE(duty_id, skill_id)')]

class DutyBehaviour(BaseModel):
    duty = ForeignKeyField(Duty, backref="duty_behaviours", on_delete="CASCADE")
    behaviour = ForeignKeyField(Behaviour, backref="behaviour_duties", on_delete="CASCADE")
    class Meta:
        constraints = [SQL('UNIQUE(duty_id, behaviour_id)')]

