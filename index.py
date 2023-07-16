from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
import httplib2

URLS_FILE = "urls.txt"
JSON_KEY_FILE = "credentials.json"

SCOPES = ["https://www.googleapis.com/auth/indexing"]
ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"

# Authorize credentials
credentials = ServiceAccountCredentials.from_json_keyfile_name(JSON_KEY_FILE, scopes=SCOPES)
http = credentials.authorize(httplib2.Http())

# Build service
service = build('indexing', 'v3', http=http)

# Read URLs from file
with open(URLS_FILE, 'r') as file:
    urls = file.read().splitlines()

# Send individual index requests for each URL
for url in urls:
    request = service.urlNotifications().publish(body={"url": url, "type": "URL_UPDATED"})
    response = request.execute()
    print(response)
