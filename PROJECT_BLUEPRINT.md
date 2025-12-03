# Supply Chain Detective

A browser-based analytics puzzle game where you investigate supply chain disruptions using real data analysis techniques.

## What is this?

I built this project to showcase practical analytics and data engineering skills in a fun, interactive format. Players act as supply chain analysts, digging through data to find root causes of shipment delays.

Think of it as a "detective game" but for data nerds.

## How the game works

1. You get a mission with a dataset of shipments
2. Explore the dashboard to spot patterns
3. Filter, drill down, investigate
4. Form a hypothesis about what's causing delays
5. Submit your answer
6. Get scored based on accuracy

## Project Structure

```
├── app.py                 # Main Streamlit entry point
├── backend/
│   ├── data_loader.py     # CSV loading + validation
│   ├── preprocess.py      # Data cleaning, feature engineering
│   ├── kpi_engine.py      # Metrics calculations
│   ├── missions.py        # Mission configs and answers
│   ├── scoring.py         # Score calculation logic
│   ├── anomaly_model.py   # IsolationForest for outlier detection
│   └── delay_predictor.py # RandomForest for delay predictions
├── frontend/
│   ├── components.py      # Reusable UI components
│   ├── dashboard_ui.py    # Dashboard view
│   ├── investigation_ui.py# Investigation mode
│   └── results_ui.py      # Score/results screen
└── utils/
    ├── constants.py
    └── helpers.py
```

## Data schema

Working with these core fields:
- shipment_id, warehouse_id, supplier
- origin, destination, distance_km
- expected_time, actual_time
- cost, sku_count, traffic_index

Additional computed fields:
- transit_time (actual - expected)
- delay_flag
- supplier_score

## Key metrics tracked

- Average delay (days/hours)
- Delay rate percentage
- Total vs late shipments
- Warehouse utilization scores
- Supplier reliability

## Tech stack

- **Python 3.x**
- **Streamlit** for the UI
- **Pandas/NumPy** for data wrangling
- **Plotly/Altair** for visualizations
- **Scikit-learn** for ML models

## ML components (optional features)

The game includes some ML-driven hints:

- **Delay predictor**: RandomForest model that estimates delay risk
- **Anomaly detector**: IsolationForest to flag unusual shipments
- Could add Prophet/ARIMA for demand forecasting later

## Scoring

- 100 points for correct answer
- -10 points per hint used
- Time bonuses possible in future versions

## Running locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deployment

Hosted on Streamlit Cloud. Just connect the GitHub repo and point to `app.py`.

## Roadmap

**Done:**
- Core dashboard and investigation UI
- Mission system with scoring
- Basic anomaly detection

**Next up:**
- More missions with varying difficulty
- Better ML integration
- Story mode with connected missions

**Maybe later:**
- User accounts / leaderboard
- Custom mission builder
