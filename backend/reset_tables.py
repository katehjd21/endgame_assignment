from pg_db_connection import pg_db, database
from models import (
    Coin, Duty, Knowledge, Skill, Behaviour,
    DutyCoin, DutyKnowledge, DutySkill, DutyBehaviour
)

database.initialize(pg_db)

pg_db.drop_tables([
    DutyCoin, DutyKnowledge, DutySkill, DutyBehaviour,
    Coin, Duty, Knowledge, Skill, Behaviour
], safe=True)

pg_db.create_tables([
    Coin, Duty, Knowledge, Skill, Behaviour,
    DutyCoin, DutyKnowledge, DutySkill, DutyBehaviour
], safe=True)

print("Tables reset successfully!")