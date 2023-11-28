# -------------------------------------------------------------------------
# FILENAME: db_connection.py
# SPECIFICATION: Connect to a database and manipulate the NoSQL database
# FOR: CS 4250- Group Project
# TIME SPENT: 2 min
# -----------------------------------------------------------*/

# importing some Python libraries
from pymongo import MongoClient


def connectDataBase():
    # Create a database connection object using pymongo
    DB_NAME = 'biology_department'
    DB_HOST = 'localhost'
    DB_PORT = 27017

    try:
        # Create an instance of MongoClient
        client = MongoClient(host=DB_HOST, port=DB_PORT)
        # Create a database
        db = client[DB_NAME]
        return db
    except:
        print('Database not connected successfully')
