# Trading Economics GDP Analysis Backend

## Overview
Python FastAPI service providing GDP data analysis and visualization capabilities through the Trading Economics API. This service powers the frontend visualization system for GDP trends across selected countries.

## Features
- Historical GDP data retrieval
- Statistical analysis including YoY growth rates
- Polynomial regression for trend analysis
- RESTful API endpoints
- Docker containerization

## Tech Stack
- Python 3.12
- FastAPI
- pandas
- scikit-learn
- Trading Economics API
- Docker

## Installation
1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
Run the development server:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Or use Docker:
```bash
docker build -t te-backend .
docker run -p 8000:8000 te-backend
```

## API Endpoints
- `GET /gdp/{country}`: Retrieve GDP data and analysis for specified country
- `GET /`: Health check endpoint

## Environment
- Python 3.12 or higher
- Trading Economics API credentials required
- Compatible with Vue.js frontend

## License
Part of the Trading Economics API implementation.