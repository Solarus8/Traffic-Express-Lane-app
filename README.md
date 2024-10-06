# Traffic Tips!
This project serves as the backend for the **Traffic Tips!** app.<br>
The app is designed to help drivers decide if they should pay for the express lanes on the freeways in Denver.<br>
It currently includes and API. Later it will also include a database connection for saving user data and a data analytics part to make the app even better.

## Project Setup
1. `cd project_directory` to change into the directory where the project should be
2. `git clone https://github.com/Solarus8/Traffic-Express-Lane-app.git`
3. enter username and password
4. copy `example.env` and name it `.env`, replace values as needed
5. `pip install --user pipenv` to install pipenv
6. `pipenv install` to install all requirements

## API
### How to use it
`python -m uvicorn run_api:app --reload` to run it, making it reload automatically when you save a file.<br>
The file `run_api.py` is the root of it all.<br>
The folder `api` contains all components of the API.<br>
The folder `common` contains everything that may not be unique to the API.<br>

### Endpoints
Replace `<domain>` with our own domain or `127.0.0.0:8000` if you are testing locally.
#### recommend
**request**<br>
URL: `GET <domain>/api/recommend`
Body: {"name": "name of gate", "session_id": "ID of app session", "fingerprint": "ID of phone used"}
Example: Look at `test/get_recommend_express_lane.http`
**response example**<br>
{
  "name": "Lowell (West Bound)",
  "start_coordinate": "39.835657,-105.022941",
  "end_coordinate": "39.842883,-105.040233",
  "route": "US36 WB",
  "recommend": false,
  "estimated_time_saving": -3,
  "comment": "Not recommended"
}


#### trip
**request**<br>
URL: `POST <domain>/api/trip`
Example: Look at `test/post_trip_data.http`
**response**<br>
null


## Useful Links
https://capacitorjs.com/docs/apis/geolocation.
