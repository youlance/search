from os import environ
from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import LimitOffsetPage, Page, add_pagination, paginate

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pwd = environ.get("PGPASSWORD")
usr = environ.get("PGUSER")
prt = environ.get("PGPORT")
nam = environ.get("PGNAME")


class Result(BaseModel):
    name: str
    username: str
    picture: str


while True:
    try:
        connection = psycopg2.connect(host='localhost', port=prt, database=nam, user=usr, password=pwd,
                                      cursor_factory=RealDictCursor)
        cursor = connection.cursor()
        print("connection successful!")
        break
    except Exception as error:
        print(error)
        time.sleep(2)


@app.get("/search/{name_query}", response_model=LimitOffsetPage[Result])
async def find_user(name_query: str):
    name_query = '%' + name_query + '%'
    cursor.execute(""" SELECT name,username,picture FROM profiles WHERE name LIKE %s OR username LIKE %s """,
                   (name_query, name_query))
    profiles = cursor.fetchall()

    return paginate(profiles)


add_pagination(app)
