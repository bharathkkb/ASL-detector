from pymongo import MongoClient
import sys
from pymongo.errors import ConnectionFailure
from bson import json_util, ObjectId
import os
import gridfs
import traceback
class mongoDriver():
    def connectToMongo(self):
        """ Connect to MongoDB """
        try:
            SECRET_KEY = os.environ.get('AM_I_IN_A_DOCKER_CONTAINER', False)
            if SECRET_KEY:
                client = MongoClient('mongodb:27017')
            else:
                client = MongoClient('localhost:27017')
            # print("Connected successfully")
            return client
        except ConnectionFailure as e:
            sys.stderr.write("Could not connect to MongoDB:{}".format(str(e)))
            sys.exit(1)

    def getFind(self, dbName, collectionName, query=False, exclude=False):
        """ Run a query to get data from Mongo DB """
        """ Exclude removes those keys from the data returned"""
        conn = self.connectToMongo()
        try:
            db = conn[dbName]
            collection = db[collectionName]
            if query and exclude:
                return collection.find(query, exclude)
            elif query:
                return collection.find(query)
            else:
                return collection.find()
        except ConnectionFailure as e:
            sys.stderr.write("Could not fetch from MongoDB: {}".format(str(e)))
            sys.exit(1)

    def getFindOne(self, dbName, collectionName, query=False, exclude=False):
        """ Run a query to get data from Mongo DB """
        """ Exclude removes those keys from the data returned"""
        conn = self.connectToMongo()
        try:
            db = conn[dbName]
            collection = db[collectionName]
            if query and exclude:
                return collection.find_one(query, exclude)
            elif query:
                return collection.find_one(query)
            else:
                return collection.find_one()
        except ConnectionFailure as e:
            sys.stderr.write(
                "Could not fetch one from MongoDB: {}".format(str(e)))
            sys.exit(1)

    def putDict(self, dbName, collectionName, obj):
        """ Run a query to put data into Mongo DB """
        conn = self.connectToMongo()
        try:
            db = conn[dbName]
            collection = db[collectionName]

            return collection.insert_one(obj)

        except ConnectionFailure as e:
            sys.stderr.write(
                "Could not write one to MongoDB: {}".format(str(e)))
            sys.exit(1)

    def updateDict(self, dbName, collectionName, newObj):
        """ Run a query to update data into Mongo DB """
        conn = self.connectToMongo()
        try:
            db = conn[dbName]
            collection = db[collectionName]
            for key, val in newObj.items():
                try:
                    collection.update_one({'_id': ObjectId(newObj['_id'])}, {
                                          '$set': {key: val}}, upsert=False)
                except Exception as ex:
                    print(ex)
                    print(traceback.print_exc())
                    sys.stderr.write(
                        "Error while updating: {}".format(str(ex)))
            return True

        except ConnectionFailure as e:
            sys.stderr.write(
                "Could not update one to MongoDB: {}".format(str(e)))
            sys.exit(1)



# just for testing queries
if __name__ == "__main__":
    query = dict()
    query["student_id"] = "02"
    # query = {'student_id': '02'}
    print(mongoDriver().getFindOne("peer-tutor-db", "student", query))
