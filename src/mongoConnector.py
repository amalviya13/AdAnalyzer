from pymongo import MongoClient
import json
from flask import Flask 
from flask_cors import CORS 


connection_url = "mongodb+srv://admin:coloranalyzerboissquad123yeet@cluster0.vcfdv.mongodb.net/test?retryWrites=true&w=majority"

app = Flask(__name__) 
client = pymongo.MongoClient(connection_url) 

# Database 
Database = client.get_database('companies') 
# Table 
SampleTable = Database.SampleTable 
  
if __name__ == '__main__': 
    app.run(debug=True) 

    # client = MongoClient()
    # client = MongoClient('localhost', 27017)    

    # dbname = "companies"
    # mydb = client[dbname]
    # print(client.server_info())
    # print(mydb.list_collection_names())
    # for coll in mydb.list_collection_names():
    #     print(coll)
