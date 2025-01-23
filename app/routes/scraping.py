from fastapi import APIRouter, Depends, HTTPException, Header
from app.models.notfication_channel import NotificationChannel
from app.models.scrape_request import ScrapeRequest
from app.services.notification.notify_strategy import NotificationStrategy
from app.services.scrapper_service import ScrapperService
from app.utils.db.json_file_stoage import JsonFileStorage

router = APIRouter()

AUTHORIZATION_TOKEN = "ADITYA_ATLYS_SELECTED"
BASE_URL = "https://dentalstall.com/shop/"
def authenticate(authorization: str = Header(...)):
    token = authorization.split(" ")[1]
    if token != AUTHORIZATION_TOKEN:
        raise HTTPException(status_code=401, detail= "Unauthorized")
    
@router.post("/scrape", dependencies=[Depends(authenticate)])    
def scrape(body: ScrapeRequest):
    scrapper = ScrapperService(
        base_url=BASE_URL,
        page_limit=body.page_limit,
        proxy=body.proxy,
        storage_strategy = JsonFileStorage(),
        notification_strategy = NotificationStrategy(
        [NotificationChannel.CONSOLE]
    )
    )
    scraped_products = scrapper.scrape()
    return scraped_products
