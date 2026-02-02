# Cancun Tourism Analytics

A comprehensive tourism analytics dashboard for Cancun that collects, processes, and predicts tourist arrival data using real-time APIs and machine learning models.

## Features

- Real-time data extraction from Google Trends and World Bank API
- Automated data processing and forecasting
- Interactive Streamlit dashboard with 4 main sections
- Automatic updates every 3 weeks via GitHub Actions
- Machine learning predictions for tourist arrivals
- Hotel occupancy analysis and projections

## Project Structure

```
cancun-tourism-analytics/
├── data/
│   ├── raw/                    # Raw data from APIs
│   │   ├── trends_real.csv
│   │   ├── trends_time_real.csv
│   │   └── worldbank_tourism_real.csv
│   └── processed/              # Processed data for analysis
│       ├── tourism_complete.csv
│       ├── occupancy_daily.csv
│       ├── occupancy_monthly.csv
│       ├── occupancy_predictions.csv
│       └── arrivals_forecast_2027.csv
├── src/
│   ├── extractors/
│   │   ├── trends_extractor.py
│   │   ├── worldbank_extractor.py
│   │   └── intelligent_generator.py
│   ├── models/
│   │   └── predictor.py
│   └── processors/
├── .github/
│   └── workflows/
│       └── update-data.yml     # Automated updates every 3 weeks
├── config.py                   # Project configuration
├── extract_all.py              # Main extraction script
├── streamlit_app.py            # Dashboard application
└── requirements.txt            # Python dependencies

```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/AngelAlexander25/cancun-tourism-analytics.git
cd cancun-tourism-analytics
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Data Extraction

Run the main extraction script to fetch and process all data:

```bash
python extract_all.py
```

This will:
1. Extract Google Trends data
2. Fetch World Bank tourism statistics
3. Generate complete dataset with interpolation

### Generate Predictions

Run the predictor to create forecasts:

```bash
python src/models/predictor.py
```

### Launch Dashboard

Start the Streamlit dashboard:

```bash
streamlit run streamlit_app.py
```

The dashboard will be available at `http://localhost:8501`

## Dashboard Sections

### 1. Main Dashboard
- Key metrics for 2026
- Top 10 countries by arrivals
- Historical trends 2020-2026
- Monthly hotel occupancy
- Revenue estimates
- Seasonal distribution

### 2. Detailed Predictions
- Daily occupancy predictions (next 60 days)
- Weekly analysis
- Weekday vs Weekend comparison
- 7-day forecast table

### 3. Country Analysis
- Country selector
- Historical evolution
- Growth metrics
- Google Trends interest
- Comparison with other markets

### 4. Forecast 2027
- Total arrivals projection
- Average growth rate
- Country-by-country comparison
- Detailed forecast table

## Data Sources

- **Google Trends**: Real-time search interest data by country
- **World Bank API**: Official tourism arrival statistics
- **Machine Learning Models**: scikit-learn based predictive models

## Automation

The project uses GitHub Actions to automatically update data every 3 weeks:

- Extracts fresh data from APIs
- Regenerates predictions
- Commits and pushes updated CSV files
- Streamlit Cloud auto-deploys changes

You can also trigger manual updates from the GitHub Actions tab.

## Technologies

- **Python 3.11+**
- **Streamlit**: Interactive web dashboard
- **Plotly**: Dynamic visualizations
- **Pandas**: Data manipulation
- **NumPy**: Numerical computing
- **scikit-learn**: Machine learning models
- **pytrends**: Google Trends API client
- **requests**: HTTP library for API calls

## Configuration

Target countries are defined in `config.py`:

```python
TARGET_COUNTRIES = [
    "United States", "Canada", "United Kingdom", 
    "Germany", "France", "Spain", "Brazil", 
    "Argentina", "Colombia", "Mexico"
]
```

## License

MIT License

## Author

AngelAlexander25

## Live Demo

View the live dashboard at: [Streamlit Cloud](https://cancun-tourism-analytics.streamlit.app)
