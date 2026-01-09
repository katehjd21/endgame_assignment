from pg_db_connection import pg_db
from models import Duty, Coin, Knowledge, Skill, Behaviour, DutyCoin, DutyKnowledge, DutySkill, DutyBehaviour
from peewee import *


def create_tables():
    pg_db.connect()

    tables = [
        Coin, Duty, Knowledge, Skill, Behaviour,
        DutyCoin, DutyKnowledge, DutySkill, DutyBehaviour
    ]
    pg_db.create_tables(tables, safe=True)
    print("Database tables created!")

    pg_db.close()


if __name__ == "__main__":
    create_tables()
