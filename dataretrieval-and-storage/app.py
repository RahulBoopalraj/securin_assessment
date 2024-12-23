from flask import Flask, jsonify, request
import requests
from pymongo import MongoClient

app = Flask(__name__)

mongo_client = MongoClient("mongodb://localhost:27017/")

db = mongo_client["Rahul_Securin"]
collection = db["CVEs"]

BASE_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"
RESULTS_PER_PAGE = 10  


def fetch_cve(start, total):
    #The page limit is actually 200, But here i have retrieved only 20 cves per page from the NVD API. 
    #You can change the number of cves to be retrieved by changing the value of the resultsPerPage parameter in the URL, By doing that we can able to fetch all the datas from the API.
    url = f"{BASE_URL}?resultsPerPage={total}&startIndex={start}"
    response = requests.get(url)
    data = response.json()
    return data["vulnerabilities"]



def fetch_api_data(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        print("success")
        return response.json()
    else:
        return None

@app.route("/fetch_data")
def fetch_and_store_data():
    api_data = fetch_api_data("https://services.nvd.nist.gov/rest/json/cves/2.0?resultsPerPage=20&startIndex=0")
    cve_data = api_data.get("vulnerabilities")
    # return cve_data[0]["cve"]["id"]
    for i in range(0, 20):
        data = {
            "ID": cve_data[i]["cve"]["id"],
            "Description" : cve_data[i]["cve"]["descriptions"][0]["value"],
            "Identifier": cve_data[i]["cve"]["sourceIdentifier"],
            "CPE Match" : cve_data[i]["cve"]["configurations"][0]["nodes"][0]["cpeMatch"],
            "cvssMetricV2": cve_data[i]["cve"]["metrics"]["cvssMetricV2"],
            "Published Date": cve_data[i]["cve"]["lastModified"],
            "Last Modified": cve_data[i]["cve"]["published"],
            "Staus": cve_data[i]["cve"]["vulnStatus"]
        }
        collection.insert_one(data)  
    return "Data fetched and stored successfully!"


@app.route("/", methods=["GET"])
def get_all_cves():
    start = request.args.get('start')
    total = request.args.get('total')
    
    cves = fetch_cve(start, total)
    return jsonify(cves)

def store_cves():
    #This Function will store the fetched cves into the MongoDB database.
    cves = fetch_cve()
    collection.insert_many(cves)


if __name__ == "__main__":
    app.run(debug=True)
    