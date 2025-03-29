import tradingeconomics as te
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from scipy import stats
from models import GDPResponse, GDPData
import json

class GDPService:
    def __init__(self):
        te.login('1e9879c059b3474:6hr5wpdewahqbsf')

    def calculate_regression(self, df: pd.DataFrame) -> dict:
        """Calculate regression analysis for GDP data"""
        # Convert dates to numerical values (years since start) with flexible parsing
        df['year'] = pd.to_datetime(df['DateTime'], format='mixed').dt.year
        years = (df['year'] - df['year'].min()).values.reshape(-1, 1)
        gdp_values = df['Value'].values

        # Perform linear regression
        model = LinearRegression()
        model.fit(years, gdp_values)
        
        # Calculate regression statistics
        slope, intercept, r_value, p_value, std_err = stats.linregress(
            years.flatten(), gdp_values
        )

        return {
            'slope': float(slope),  # Annual growth trend
            'r_squared': float(r_value ** 2),
            'p_value': float(p_value),
            'predicted_values': model.predict(years).tolist()
        }

    async def get_gdp_data(self, country: str, init_date: str = '2015-01-01'):
        # Get historical GDP data
        data = te.getHistoricalData(
            country=country,
            indicator=['gdp'],
            initDate=init_date,
            output_type='df'
        )
        
        # Clean and process data
        df = data[data['Country'] == 'Mexico'].copy()
        df['DateTime'] = pd.to_datetime(df['DateTime'])
        df = df.sort_values('DateTime')
        df['YoY_Growth'] = df['Value'].pct_change() * 100

        X = (df['DateTime'] - df['DateTime'].min()).dt.days.values.reshape(-1, 1)
        y = df['Value'].values
        poly = PolynomialFeatures(degree=2)
        X_poly = poly.fit_transform(X)
        model = LinearRegression()
        model.fit(X_poly, y)
        X_smooth = np.linspace(X.min(), X.max(), 100).reshape(-1, 1)
        X_smooth_poly = poly.transform(X_smooth)
        y_smooth = model.predict(X_smooth_poly)
        y_smooth_tolist = y_smooth.tolist()
        X_smooth_tolist = X_smooth.tolist()
        X_smooth_poly_tolist = X_smooth_poly.tolist()
        
        # Calculate summary statistics
        summary_stats = df['YoY_Growth'].describe().to_dict()
        summary_stats.update({
            'highest_growth': {
                'value': float(df.loc[df['YoY_Growth'].idxmax(), 'YoY_Growth']),
                'year': int(df.loc[df['YoY_Growth'].idxmax(), 'DateTime'].year)
            },
            'lowest_growth': {
                'value': float(df.loc[df['YoY_Growth'].idxmin(), 'YoY_Growth']),
                'year': int(df.loc[df['YoY_Growth'].idxmin(), 'DateTime'].year)
            }
        })
        
        # Prepare final result
        result = {
            "data": df.to_dict(orient="records"),
            "yoy_growth_summary": summary_stats,
            "X_smooth_tolist": X_smooth_tolist,
            "X_smooth_poly_tolist": X_smooth_poly_tolist,
            "y_smooth": y_smooth_tolist,
        }
        
        return json.dumps(result, default=str)

    async def compare_gdp_data(self, countries: list[str], init_date: str) -> dict:
        """Compare GDP data across multiple countries"""
        # Gather data for all countries
        country_data = {}
        for country in countries:
            country_data[country] = await self.get_gdp_data(country, init_date)
        
        # Calculate comparative metrics
        base_country = countries[0]
        comparative_metrics = {
            'relative_performance': {},
            'growth_rate_comparison': {},
            'volatility_comparison': {}
        }
        
        for country in countries[1:]:
            base_values = pd.Series([d.value for d in country_data[base_country].data])
            compare_values = pd.Series([d.value for d in country_data[country].data])
            
            # Normalize values to base country's initial value
            relative_perf = (compare_values / compare_values.iloc[0]) / (base_values / base_values.iloc[0])
            
            comparative_metrics['relative_performance'][country] = relative_perf.tolist()
            comparative_metrics['growth_rate_comparison'][country] = (
                country_data[country].growth_rate - country_data[base_country].growth_rate
            )
            comparative_metrics['volatility_comparison'][country] = (
                country_data[country].volatility / country_data[base_country].volatility
            )
        
        return {
            'countries_data': country_data,
            'comparative_metrics': comparative_metrics,
            'base_country': base_country
        }