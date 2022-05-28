import json
import requests
import config

def get_latest_block():
  return requests.get(f"{config.NXS_BASE_URL}/ledger/list/blocks", params={"limit":1, "verbose":"detail"}).json()["result"][0]

def get_block(height):
  return requests.get(f"{config.NXS_BASE_URL}/ledger/get/block?height={height}").json()["result"]

def pp(_json):
    json.dumps(_json, indent=1)
