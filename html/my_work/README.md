# Trading Economics GDP Visualization

## Overview
A Vue.js 3 application for visualizing GDP data and trends across selected countries using the Trading Economics API. The project provides interactive charts, statistical analysis, and real-time data visualization.

## Features
- Interactive GDP visualization with Chart.js
- Statistical analysis including YoY growth rates
- Country selection between Mexico, New Zealand, Sweden, and Thailand
- Date range selection with calendar
- Polynomial regression trend analysis
- Responsive Material Design UI using Vuetify 3

## Tech Stack
- Vue.js 3
- Vuetify 3
- Chart.js
- Vue Router
- Trading Economics API

## Project Structure
```
src/
    ├── components/        # Vue components
    │   ├── GDPChart.vue       # GDP visualization chart
    │   ├── GDPStats.vue       # Statistical analysis display
    │   ├── ListComponent.vue  # Country selection list
    │   ├── SkeletonLoader.vue # Loading placeholder
    │   └── SmoothChart.vue    # Main chart container
    ├── pages/            # Route pages
    ├── plugins/          # Vue plugins config
    ├── router/           # Route configuration
    ├── styles/           # Global styles
    └── App.vue          # Root component
```

## Setup
1. Install dependencies:
```bash
npm install
```

2. Run development server:
```bash
npm run dev
```

3. Build for production:
```bash
npm run build
```

## Development
- Uses ESLint for code quality
- Prettier for code formatting
- Vue Router for navigation
- Vite as build tool

## Requirements
- Node.js >= v16
- npm >= v7

## License
This project is part of the Trading Economics API implementation.