from flask import Flask, render_template
from pymongo import MongoClient

app = Flask(__name__)


client = MongoClient("mongodb://localhost:27017/") 
db = client["Rahul_Securin"]  
collection = db["cve_with_metrics"] 

@app.route('/', methods=('GET', 'POST'))
def index():
    cves = collection.find()
    print(cves[0]["ID"])
    return render_template('index.html', cves=cves)


@app.route('/<cve>', methods=('GET', 'POST'))
def profile(cve):
    query = {"ID": cve}  
    data = list(collection.find(query))
    print(data)
    return render_template('cve_info.html', cve=cve, data=data)