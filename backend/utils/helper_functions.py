from models import DutyCoin, DutyKnowledge, DutySkill, DutyBehaviour, Coin, Duty, Knowledge, Skill, Behaviour
import re

def clear_tables():
    tables_to_clear = [
        DutyCoin, DutyKnowledge, DutySkill, DutyBehaviour,
        Coin, Duty, Knowledge, Skill, Behaviour
    ]
    for table in tables_to_clear:
        table.delete().execute()