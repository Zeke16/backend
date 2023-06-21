from pymongo import MongoClient

# Db local
# db_connection = MongoClient().local

# Db en la nube

db_connection = MongoClient(
    "mongodb+srv://zeke16:NU63BHEGftKHX0oR@cluster01.ufhghso.mongodb.net/?retryWrites=true&w=majority").test
