from pymongo import MongoClient
from dotenv import load_dotenv
import os
load_dotenv()

# Db local
# db_connection = MongoClient().local

# Db en la nube

db_connection = MongoClient(os.environ.get("dbconnectionstring")).test
