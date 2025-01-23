## Steps to run the scraping api

1) Enable venv - This is to install dependencies in isolation
    Steps to create Virtual env
    1) python -m venv venv
    2) source venv/bin/activate

4) Install the following dependencies
    1) pip install fastapi uvicorn
    2) pip install beautifulsoup4
    3) pip install requests

## Run the server

uvicorn app.main:app --reload

Hit -  http://127.0.0.1:8000/scrape
