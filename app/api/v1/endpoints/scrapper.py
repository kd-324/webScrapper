from typing import List
from fastapi import APIRouter, Depends, HTTPException, Security, status
from fastapi.responses import JSONResponse

from app.constants.constants import API_KEY
from app.models.product import Product
from app.models.request.scrape_request import ScrapeRequest
from app.utils.dependencies import get_scrapper_service
from app.services.scrapper_service import ScrapperService
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter()

def verify_token(credentials: HTTPAuthorizationCredentials = Security(HTTPBearer())):
    token = credentials.credentials
    if token != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token

@router.post("/scrape")
async def scrape_webpage(scrape_request: ScrapeRequest, scrapper_service: ScrapperService = Depends(get_scrapper_service), token: str = Depends(verify_token)):
    try:
        await scrapper_service.scrape_website(scrape_request.page_count, scrape_request.proxy_string)
        return JSONResponse(
            content={"status": "success"},
            status_code=200
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/products", response_model=List[Product])
async def get_product_list(scrapper_service: ScrapperService = Depends(get_scrapper_service), token: str = Depends(verify_token)):
    try:
        product_list = await scrapper_service.list_products()
        return JSONResponse(
            content=product_list,
            status_code=200
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/healthcheck")
async def healthcheck():
    return JSONResponse(
        content={"status": "up"},
        status_code=200
    )