from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from threading import Thread
import requests
import asyncio

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

baseGoogleUrl = "https://maps.googleapis.com/maps/api/geocode/json"
baseStravaUrl = "https://www.strava.com/api/v3"
googleKey = "Your Google API key"
stravaKey = "Your Strava API key"

segments = []

class Segment(BaseModel):
    name: str = None
    distance: float = None
    elevation: float = None
    avg_grade: float = None
    no_efforts: int = None
    no_athletes: int = None
    no_stars: int = None
    kom: str = None
    qom: str = None
    ll: str = None
    ll_no_efforts: int = None

@app.get('/segments/address={address}&radius={radius}&type={type}')
async def getSegments(address: str, radius: int, type: str):
    coordinates = await getAddressCoordinates(address)
    print(coordinates.values())
    areaCoordinates = countAreaCoordinates(*coordinates.values(), radius)
    print("Coordinates: ", *areaCoordinates["leftDownCorner"].values(), *areaCoordinates["rightUpCorner"].values())
    segments_data = await exploreSegments(
        *areaCoordinates["leftDownCorner"].values(), *areaCoordinates["rightUpCorner"].values(),
        type
    )
    segments.clear()
    await fillSegments(segments_data["segments"])
    return {"results": sorted(segments, key=lambda x: x.no_efforts, reverse=True)}

@app.get('/address/{address}')
async def getAddressCoordinates(address: str):
    
    PARAMS = {'address': address, 'key': googleKey}

    r = requests.get(url = baseGoogleUrl, params = PARAMS)
    data = r.json()
    
    results = {}
    results["latitude"] = data["results"][0]["geometry"]["location"]["lat"]
    results["longitude"] = data["results"][0]["geometry"]["location"]["lng"]

    return results

@app.get('/segments/ldc_lat={ldc_lat}&ldc_lng={ldc_lng}&ruc_lat={ruc_lat}&ruc_lng={ruc_lng}')
async def exploreSegments(ldc_lat: float, ldc_lng: float, ruc_lat: float, ruc_lng: float, activity_type: str):
    URL = baseStravaUrl + "/segments/explore"

    bounds = [float(ldc_lat), float(ldc_lng), float(ruc_lat), float(ruc_lng)]

    PARAMS = {'bounds': ','.join(map(str, bounds)), 'activity_type': activity_type}
    print(PARAMS)
    HEADERS = {'Authorization': 'Bearer ' + stravaKey}

    r = requests.get(url = URL, params = PARAMS, headers = HEADERS)
    segments_data = r.json()
    return segments_data

@app.get('/segment/{segment_id}')
async def getSegment(segment_id: int):
    URL = baseStravaUrl + "/segments/" + str(segment_id)

    HEADERS = {'Authorization': 'Bearer ' + stravaKey}

    r = requests.get(url = URL, headers = HEADERS)
    segment_data = r.json()
    return segment_data

def countAreaCoordinates(longitude: float, latitude: float, radius: int):
    leftDownCorner = {}
    leftDownCorner["longitude"] = longitude - radius * 360 / 40000
    leftDownCorner["latitude"] = latitude - radius * 180 / 40000

    rightUpCorner = {}
    rightUpCorner["longitude"] = longitude + radius * 360 / 40000
    rightUpCorner["latitude"] = latitude + radius * 180 / 40000

    return {"leftDownCorner": leftDownCorner, "rightUpCorner": rightUpCorner}

async def segmentDataInThread(segment: dict):
    print(segment)
    seg = Segment(
        name=segment["name"],
        distance=segment["distance"],
        elevation=segment["elev_difference"],
        avg_grade=segment["avg_grade"]
    )
    segmentDetails = await getSegment(segment['id'])
    print(segmentDetails)
    seg.no_efforts = segmentDetails["effort_count"]
    seg.no_athletes = segmentDetails["athlete_count"]
    seg.no_stars = segmentDetails["star_count"]
    if (segmentDetails["xoms"] is not None):
        seg.kom = segmentDetails["xoms"]["kom"] if segmentDetails["xoms"]["kom"][:-1] < segmentDetails["xoms"]["qom"][:-1] else segmentDetails["xoms"]["qom"]
        seg.qom = segmentDetails["xoms"]["qom"]
    if (segmentDetails["local_legend"] is not None):
        seg.ll = segmentDetails["local_legend"]["title"]
        seg.ll_no_efforts = int(segmentDetails["local_legend"]["effort_count"])
    segments.append(seg)

async def fillSegments(data: str):
    threads = []
    for segment in data:
        thread = Thread(target=asyncio.run, args=(segmentDataInThread(segment),))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()