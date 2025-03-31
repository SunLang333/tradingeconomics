from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from services import GDPService  # Changed from relative to absolute import
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost"],  # Only allow localhost for better safety in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

gdp_service = GDPService()

@app.get("/gdp/{country}")
async def get_gdp_data(
    country: str, 
    init_date: str = Query(default='2015-01-01', description="Initial date in YYYY-MM-DD format")
):
    return await gdp_service.get_gdp_data(country, init_date)

@app.get("/")
async def root():
    return {"message": "It's on!"}