from pymongo import MongoClient
import pymongo
import json
from flask import Flask 
from flask_cors import CORS 


connection_url = "mongodb+srv://admin:coloranalyzerboissquad123yeet@cluster0.vcfdv.mongodb.net/test?retryWrites=true&w=majority"

app = Flask(__name__) 
client = pymongo.MongoClient(connection_url) 

companiesDB = client["companies"]
print(companiesDB.list_collection_names())
# Database 
Database = client.get_database('companies') 
# Table 
SampleTable = Database.SampleTable 
  
if __name__ == '__main__': 
    app.run(debug=True) 
