from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

segments = []

@app.get('/segments/address={address}_radius={radius}_type={type}/')
async def getSegments(address: str, radius: int, type: str):
    coordinates = await getCityCoordinates(address)
    # URL = "http://127.0.0.1:8000/address/"
    # PARAMS = {'address': address}
    # r = requests.get(url = URL, params = PARAMS)
    # coordinates = r.json()
    return coordinates

@app.get('/address/{address}')
async def getCityCoordinates(address: str):
    URL = "https://maps.googleapis.com/maps/api/geocode/json"
    key = "Your API key"
    
    PARAMS = {'address': address, 'key': key}

    r = requests.get(url = URL, params = PARAMS)
    data = r.json()
    results = {}
    results["longitude"] = data["results"][0]["geometry"]["location"]["lng"]
    results["latitude"] = data["results"][0]["geometry"]["location"]["lat"]
    return results
