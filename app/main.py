from os import environ
from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

pwd = environ.get("YOULANCE")

while True:
    try:
        connection = psycopg2.connect(host='localhost', database='profiles', user='postgres', password=pwd,
                                      cursor_factory=RealDictCursor)
        cursor = connection.cursor()
        print("connection successful!")
        break
    except Exception as error:
        print(error)
        time.sleep(2)


@app.get("/search/{name_query}")
async def find_user(name_query: str):
    name_query = '%' + name_query + '%'
    cursor.execute(""" SELECT name,username,picture FROM profiles WHERE name LIKE %s OR username LIKE %s LIMIT 10 """,
                   (name_query, name_query))
    profiles = cursor.fetchall()
    return {"Profiles": profiles}
