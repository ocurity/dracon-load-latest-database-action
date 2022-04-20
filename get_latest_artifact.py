import requests
from dateutil import parser
import os
import zipfile
from pprint import pprint

repo="https://api.github.com/repos/northdpole/artifacttests/actions/artifacts"
artifacts = requests.get(repo).json()['artifacts']

latest = parser.isoparse(artifacts[-1]['updated_at'])
artifact_url = artifacts[-1]["archive_download_url"]
for art in artifacts:
    if "dracon_enrichment_db" not in art["name"]:
        continue
    d =parser.isoparse(art['updated_at'])
    if d > latest:
        latest = d
        artifact_url = art["archive_download_url"]

token = os.environ["GH_ACCESS_TOKEN"]
header={"Authorization" :"token %s"%token}
resp = requests.get(artifact_url, stream=True,headers=header)
with open("/tmp/latest.zip", "wb") as zip:
    for chunk in resp.iter_content():
        zip.write(chunk)

with zipfile.ZipFile("/tmp/latest.zip") as zip:
    zip.extractall(os.environ["OUTPUT_DIR"])
