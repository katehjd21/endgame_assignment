from dotenv import load_dotenv
from peewee import *
import os

load_dotenv()

pg_db = PostgresqlDatabase(
    os.getenv('DATABASE'),
    user=os.getenv('DB_USERNAME'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('HOST'),
    port=int(os.getenv('PORT'))
)

