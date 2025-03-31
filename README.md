# Trading Economics API Implementation

## Overview
This project implements a comprehensive data visualization system utilizing the Trading Economics API. The live deployment can be accessed at [te.dtianhao.win](https://te.dtianhao.win).

## Architecture

### Backend (Python)
- FastAPI server delivering GDP data analysis
- Docker containerization for consistent deployment
- Polynomial regression analysis for trend prediction
- Statistical computations including YoY growth rates

### Frontend (Vue.js 3)
- Vuetify 3 for Material Design components
- Interactive GDP visualization using Chart.js
- Real-time data updates and smooth transitions
- Responsive layout for various screen sizes

## Features
- GDP trend analysis for Mexico, New Zealand, Sweden, and Thailand
- Interactive date range selection
- Statistical insights including:
    - Year-over-Year growth rates
    - Trend analysis with polynomial regression
    - Key statistical indicators

## Technical Stack
- **Backend**: Python, FastAPI, scikit-learn, pandas
- **Frontend**: Vue 3, Vuetify, Chart.js
- **Deployment**: Docker, Nginx
- **API**: Trading Economics API

## Live Demo
Visit [te.dtianhao.win](https://te.dtianhao.win) to explore the implementation.
