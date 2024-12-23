## 1. CVE Data Retrieval and Storage

This Flask API retrieves and stores Common Vulnerabilities and Exposures (CVEs) data from the National Vulnerability Database (NVD).

### Endpoints

- **`/fetch_store_data` (GET):** Fetches and stores CVE data from the NVD API.
  - Query parameters:
    - `start` (optional, integer): The starting index for fetching CVEs (defaults to 0).
    - `total` (optional, integer): The number of CVEs to fetch (defaults to 20).
  - Response: Success message.
- **`/` (GET):** Retrieves all CVEs stored in the MongoDB collection.
  - Query parameters:
    - `start` (optional, integer): The starting index for retrieving CVEs (defaults to 0).
    - `total` (optional, integer): The number of CVEs to retrieve (defaults to 20).
  - Response: List of CVEs in JSON format.

### Configuration

- **MongoDB:**
  - The script requires a MongoDB connection string (`MONGO_URI`) to be set in the environment.
  - The database name (`DB_NAME`) and collection name (`COLLECTION_NAME`) are defined in the script.

### Running the Script

1. Set the `MONGO_URI` environment variable with your MongoDB connection string.
2. Run the script using `flask run`.

This will start the Flask development server and make the API endpoints accessible.

## 2. CVE Data API

This Flask API provides access to a collection of Common Vulnerabilities and Exposures (CVEs) stored in a MongoDB database.

### Endpoints

- **`/api/cve_data` (GET):** Retrieves all CVE data from the database.
  - Response: JSON list of all CVEs.
- **`/api/cve_data/<cve_id>` (GET):** Fetches a specific CVE by its ID.
  - Path parameter:
    - `<cve_id>`: The ID of the CVE to retrieve.
  - Response: JSON object containing the CVE data, or a 404 error message if not found.
- **`/api/cve_data/recent/<int:days>` (GET):** Retrieves CVEs that have been modified within the last `days`.
  - Path parameter:
    - `<int:days>`: The number of days to look back for recent CVEs.
  - Response: JSON list of recent CVEs.

### Configuration

- **MongoDB:**
  - The script requires a MongoDB connection string (`MONGO_URI`) to be set in the environment.
  - The database name (`DB_NAME`) and collection name (`COLLECTION_NAME`) are defined in the script and should be replaced with your actual values.

### Running the Script

1. Set the `MONGO_URI` environment variable with your MongoDB connection string.
2. Replace `your_mongo_uri_here`, `your_db_name_here`, and `your_collection_name_here` with your actual values in the script.
3. Run the script using `flask run`.

This will start the Flask development server and make the API endpoints accessible.

## 3. CVE Web Application

This Flask application provides a web interface to explore a collection of Common Vulnerabilities and Exposures (CVEs) stored in a MongoDB database.

### Dependencies

- Flask
- pymongo

### Configuration

- **MongoDB:**
  - The script requires a MongoDB connection string (`MONGO_URI`) to be set in the environment.
  - The database name (`DB_NAME`) and collection name (`COLLECTION_NAME`) are defined in the script and should be replaced with your actual values.

### Running the Application

1. Set the `MONGO_URI` environment variable with your MongoDB connection string.
2. Replace `your_mongo_uri`, `your_database_name`, and `your_collection_name` with your actual values in the script.
3. Run the script using `flask run`.

This will start the Flask development server and make the application accessible at `http://127.0.0.1:5000/`.

### Usage

The application provides two main functionalities:

- **List all CVEs:** The root path (`/`) displays a table containing all CVEs in the database. Each entry includes the CVE ID, identifier, published date, last modified date, and status. Clicking on the CVE ID leads to the detailed information page.
- **View a specific CVE:** Clicking on a CVE ID in the list view opens a detailed page for that particular CVE. This page displays the CVE description, CVSS v2 metrics (including severity score, vector string, and detailed metrics for each category), exploitability and impact scores, and CPE information.

**Note:** You may need to adjust the CSS styling in the HTML templates (`index.html` and `cve_info.html`) to match your preferences.
