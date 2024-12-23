from flask import Flask, render_template
from pymongo import MongoClient

app = Flask(__name__)

MONGO_URI = "your_mongo_uri"
DB_NAME = "your_database_name"
COLLECTION_NAME = "your_collection_name"

# Database connection
client = MongoClient(MONGO_URI)
db = mongo_client[DB_NAME]
collection = db[COLLECTION_NAME]

@app.route('/', methods=['GET'])
def index():
    """
    Route to display all CVEs.
    """
    cves = collection.find()
    return render_template('index.html', cves=cves)

@app.route('/<cve>', methods=['GET'])
def profile(cve):
    """
    Route to display details of a specific CVE.
    """
    query = {"ID": cve}
    data = list(collection.find(query))
    return render_template('cve_info.html', cve=cve, data=data)

if __name__ == '__main__':
    app.run(debug=True)
