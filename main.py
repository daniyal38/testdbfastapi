import os
from fastapi import FastAPI, Depends
import pymysql

app = FastAPI()

def get_db():
    connection = pymysql.connect(
        host="testsqlserverdaniyal38.mysql.database.azure.com",
        user="daniyal",
        password="Up32hl9989",
        database="fastapidb",
        port=3306,
        ssl={"ssl": {}}
    )
    try: 
        yield connection
    finally:
        connection.close()

def run_query(db, sql, params=None, fetch="all"):
    cur = db.cursor()
    cur.execute(sql, params or ())
    if fetch == "one":
        result = cur.fetchone()
    elif fetch == "all":
        result = cur.fetchall()
    else:
        db.commit()
        result = {"status": "success"}
    cur.close()
    return result


@app.get('/')
def test_conn():
    return {'message':'connection'}

@app.get("/users")
def get_users_info(db=Depends(get_db)):
    result = run_query(db, "SELECT * FROM users")
    return {"users": result}

@app.post("/new_user")
def post_user_info(name: str, email: str, db=Depends(get_db)):
    insert_query = "INSERT INTO users (name, email) VALUES (%s, %s)"
    run_query(db, insert_query, params=(name, email), fetch=None)
    return {"message": f"User {name} added successfully"}
