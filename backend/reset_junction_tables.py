from pg_db_connection import pg_db
from models import DutyCoin, DutyKnowledge, DutySkill, DutyBehaviour

pg_db.drop_tables([DutyCoin, DutyKnowledge, DutySkill, DutyBehaviour], safe=True)

pg_db.create_tables([DutyCoin, DutyKnowledge, DutySkill, DutyBehaviour], safe=True)

print("Junction tables reset successfully!")
