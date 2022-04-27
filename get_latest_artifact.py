
import requests
from dateutil import parser
import os
import zipfile
from pprint import pprint
import logging
logging.basicConfig(level=logging.DEBUG)
repo=f"https://api.github.com/repos/{os.environ['INPUT_REPO']}/actions/artifacts"

print(f"retrieving artifacts from repo {repo}")

artifacts = requests.get(repo).json()['artifacts']
latest = parser.isoparse(artifacts[-1]['updated_at'])
artifact_url = None
for art in artifacts:
    if art.expired == "true" and "dracon_enrichment_db" not in art["name"]:
        continue
    d =parser.isoparse(art['updated_at'])
    if d > latest:
        latest = d
        artifact_url = art["archive_download_url"]

if not artifact_url:
    print("Did not find a Dracon DB, this is not fatal as the enricher will create it, exiting")
    exit(0)

pprint( os.environ["ACTIONS_RUNTIME_TOKEN"] == os.environ["INPUT_GH_ACCESS_TOKEN"])
token =  os.environ["INPUT_GH_ACCESS_TOKEN"]
pprint(f"{','.join([t for t in token])}")
if len(token) == 0:
    pprint("empty token")
resp = requests.get(artifact_url, stream=True,headers={"Authorization" :"token %s"%token})
if resp.status_code == 200:
    pprint("success!!!!")
elif resp.status_code != 200:
    print("Error receiving files for artifact %s"%artifact_url)
    print(resp.status_code)
    pprint(requests.get(artifact_url).json())
    raise ValueError

with open("/tmp/latest.zip", "wb") as fl:
    for chunk in resp.iter_content():
        fl.write(chunk)
try:
    with zipfile.ZipFile("/tmp/latest.zip") as zip:
        print("Extracting files to %s"%os.environ["INPUT_OUTPUT_DIR"])
        zip.extractall(os.environ["INPUT_OUTPUT_DIR"])

    print("Files extracted, dir contents are:")
    pprint(os.listdir(os.environ["INPUT_OUTPUT_DIR"]))
except zipfile.BadZipFile as bzf:
    with open("/tmp/latest.zip") as l:
        pprint(l.read())