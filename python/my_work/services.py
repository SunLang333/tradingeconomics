import tradingeconomics as te
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from scipy import stats
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
        df = data[data['Country'].isin(['Mexico', 'New Zealand', 'Sweden', 'Thailand'])].copy()
        df['DateTime'] = pd.to_datetime(df['DateTime'])
        df = df.sort_values('DateTime')
        
        # Calculate YoY growth and handle NaN values
        df['YoY_Growth'] = df['Value'].pct_change() * 100
        df['YoY_Growth'] = df['YoY_Growth'].fillna(-1)  # Fill NaN with -1

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
        
        # Ensure we have valid values for extremes
        max_idx = df['YoY_Growth'].idxmax()
        min_idx = df['YoY_Growth'].idxmin()
        
        if pd.notna(max_idx) and pd.notna(min_idx):
            summary_stats.update({
                'highest_growth': {
                    'value': float(df.loc[max_idx, 'YoY_Growth']),
                    'year': int(df.loc[max_idx, 'DateTime'].year)
                },
                'lowest_growth': {
                    'value': float(df.loc[min_idx, 'YoY_Growth']),
                    'year': int(df.loc[min_idx, 'DateTime'].year)
                }
            })
        else:
            summary_stats.update({
                'highest_growth': {'value': -1, 'year': -1},
                'lowest_growth': {'value': -1, 'year': -1}
            })
        
        # Prepare final result
        result = {
            "data": df.to_dict(orient="records"),
            "yoy_growth_summary": summary_stats,
            "X_smooth_tolist": X_smooth_tolist,
            "X_smooth_poly_tolist": X_smooth_poly_tolist,
            "y_smooth": y_smooth_tolist,
        }
        
        # Custom JSON encoder to handle any remaining NaN values
        def custom_json_encoder(obj):
            if pd.isna(obj):
                return -1
            return str(obj)
        
        return json.dumps(result, default=custom_json_encoder)
