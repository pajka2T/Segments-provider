# Segments provider 🏃  
API providing data of Strava's segments near specified place and a simple website showing how it works.

## About the project  
This API provides an easy way to gather the data of Strava's segments. You just need to fill in the address of a place you want to explore, choose the radius of an area in which you are looking for segments and select the type of sport you are interested in: running or cycling. Then you will be provided with the most important data of segments. That's it! Go on and check the segments' KOMs and local legends, and try to beat them in your activities! 🏁  

---
I created this API using **Python**, **FastAPI** and **REST** for gathering data, **Bootstrap** and **HTML** for frontend along with **JavaScript** script for showing data on the website.  
It would not be possible without the [Google Geocoding API](https://github.com/googlemaps/google-maps-services-python?tab=readme-ov-file) 🚩, for getting coordinates of an address, and the [Strava API](https://developers.strava.com/) 📙 for acquiring data of segments.

## What's next?
Right now the API is working only when you provide API keys for both APIs (Google Geocoding and Strava). I am planning to expand it, so you would not have to provide these keys.

