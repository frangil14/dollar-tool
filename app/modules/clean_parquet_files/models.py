import os
from datetime import datetime, timedelta
import time

from app.utils.blob_connector import LOCAL_BLOB_PATH

class CleanParquetFiles():

    def __init__(self, logger, mongo_connector=None):
        self.logger = logger
        self.mongo_connector = mongo_connector

    def get_parquets_to_clean(self):

        date = datetime.today() - timedelta(days=5)

        self.mongo_connector.set_container('cache')
        records = self.mongo_connector.my_container.find({"ModifiedOn": {'$lte': date}}).sort('ModifiedOn', -1)
        return records

    def get_last_used_parquets(self):

        date = datetime.today() - timedelta(days=5)

        self.mongo_connector.set_container('cache')
        records = self.mongo_connector.my_container.find({"ModifiedOn": {'$gte': date}}).sort('ModifiedOn', -1)
        return records

    def get_parquets_in_server(self):
        path = LOCAL_BLOB_PATH
        output = getListOfFiles(path)
        return output

    def remove_record(self, id):
        self.mongo_connector.set_container('cache')
        myquery = {"_id": id}

        if self.mongo_connector.my_container.count_documents(myquery) > 0:
            self.mongo_connector.my_container.delete_one(myquery)

def getListOfFiles(dirName):
    # create a list of file and sub directories names in the given directory
    listOfFile = os.listdir(dirName)
    allFiles = list()

    # Iterate over all the entries
    for entry in listOfFile:

    # Create full path
        fullPath = os.path.join(dirName, entry)

    # If entry is a directory then get the list of files in this directory
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            accessTimesinceEpoc = os.path.getatime(fullPath)
            accessTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(accessTimesinceEpoc))

            allFiles.append([ fullPath, accessTime ])

    return allFiles