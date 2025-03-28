from fastapi import FastAPI
import tradingeconomics as te
import pandas as pd

app = FastAPI()

te.login('1e9879c059b3474:6hr5wpdewahqbsf')

@app.get('/')
async def root():
    return {'message': 'Hello World'}

@app.get('/getIndicatorData/{indicators}')
async def read_item(indicators: str):
    data = te.getIndicatorData(indicators=indicators)
    return data

@app.get('/getIndicatorData/{indicators}')
async def read_item(indicators: str):
    data = te.getIndicatorData(indicators=indicators)
    return data

@app.get('/getIndicatorData/{country}/{indicator}')
async def read_item(country: str, indicator: str):
    data = te.getIndicatorData(country=country, indicator=indicator)
    return data

@app.get('/getIndicatorByCategoryGroup/{country}/{category_group}')
async def read_item(country: str, category_group: str):
    data = te.getIndicatorByCategoryGroup(country=country, category_group=category_group)
    return data

@app.get('/getIndicatorByTicker/{ticker}')
async def read_item(ticker: str):
    data = te.getIndicatorByTicker(ticker=ticker)
    return data