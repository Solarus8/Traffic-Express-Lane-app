# Traffic Tips!
## Project Setup
1. `cd project_directory` to change into the directory where the project should be
2. `git clone https://github.com/Solarus8/Traffic-Express-Lane-app.git`
3. enter username and password
4. copy `example.env` and name it `.env`, replace values as needed
5. `pip install --user pipenv` to install pipenv
6. `pipenv install` to install all requirements

## API
### How to use it
`python -m uvicorn run_api:app --reload` to run it.<br>
The file `run_api.py` is the root of it all.<br>
The folder `api` contains all components of the API.<br>
The folder `common` contains everything that may not be unique to the API.<br>

We only have one endpoint so far, which is a websocket.
It can be called with `<domain>/api/recommend?user_id=<id>`, where `<domain>` is the domain and `<id>`
is the user ID created by the frontend.
It expects a JSON string when sending information to it, which should contain coordinate information
as in https://capacitorjs.com/docs/apis/geolocation.
