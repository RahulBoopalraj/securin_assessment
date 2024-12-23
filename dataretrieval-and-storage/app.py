from flask import Flask, jsonify, request
import requests
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB Configuration
MONGO_URI = "your_mongo_uri"
DB_NAME = "your_database_name"
COLLECTION_NAME = "your_collection_name"

mongo_client = MongoClient(MONGO_URI)
db = mongo_client[DB_NAME]
collection = db[COLLECTION_NAME]

# NVD API Configuration
BASE_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"
RESULTS_PER_PAGE = 20  # Adjust as needed


def fetch_cve(start=0, total=RESULTS_PER_PAGE):
    """
    Fetch CVEs from the NVD API.

    :param start: The starting index for fetching CVEs.
    :param total: The number of CVEs to fetch.
    :return: List of CVEs.
    """
    url = f"{BASE_URL}?resultsPerPage={total}&startIndex={start}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("vulnerabilities", [])
    else:
        response.raise_for_status()


def store_cve_data(cve_data):
    """
    Store CVE data into the MongoDB collection.

    :param cve_data: List of CVE data to store.
    """
    for cve in cve_data:
        data = {
            "ID": cve["cve"].get("id"),
            "Description": cve["cve"].get("descriptions", [{}])[0].get("value"),
            "Identifier": cve["cve"].get("sourceIdentifier"),
            "CPE Match": cve["cve"].get("configurations", [{}])[0].get("nodes", [{}])[0].get("cpeMatch", []),
            "cvssMetricV2": cve["cve"].get("metrics", {}).get("cvssMetricV2"),
            "Published Date": cve["cve"].get("published"),
            "Last Modified": cve["cve"].get("lastModified"),
            "Status": cve["cve"].get("vulnStatus"),
        }
        collection.insert_one(data)


@app.route("/fetch_store_data", methods=["GET"])
def fetch_and_store_data():
    """
    Endpoint to fetch and store CVE data from the NVD API.

    :return: Success message.
    """
    start_index = int(request.args.get("start", 0))
    total = int(request.args.get("total", RESULTS_PER_PAGE))

    cve_data = fetch_cve(start=start_index, total=total)
    store_cve_data(cve_data)

    return "Data fetched and stored successfully!"


@app.route("/", methods=["GET"])
def get_all_cves():
    """
    Endpoint to retrieve all CVEs stored in the MongoDB collection.

    :return: List of CVEs in JSON format.
    """
    start = int(request.args.get("start", 0))
    total = int(request.args.get("total", RESULTS_PER_PAGE))

    cve_data = list(collection.find().skip(start).limit(total))
    for item in cve_data:
        item["_id"] = str(item["_id"])  # Convert ObjectId to string for JSON serialization

    return jsonify(cve_data)


if __name__ == "__main__":
    app.run(debug=True)
