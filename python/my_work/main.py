from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from services import GDPService  # Changed from relative to absolute import
from models import GDPResponse

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vue.js default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

gdp_service = GDPService()

@app.get("/api/gdp/{country}")
async def get_gdp_data(
    country: str, 
    init_date: str = Query(default='2015-01-01', description="Initial date in YYYY-MM-DD format")
):
    return await gdp_service.get_gdp_data(country, init_date)

@app.get("/api/gdp/compare/{countries}")
async def compare_gdp(
    countries: str,
    init_date: str = Query(default='2015-01-01', description="Initial date in YYYY-MM-DD format")
):
    country_list = countries.split(",")
    return await gdp_service.compare_gdp_data(country_list, init_date)