# 🎮 Supply Chain Detective — Analytics Puzzle Game

## 1️⃣ Project Summary

Supply Chain Detective is a browser-based, data-driven investigation game where players act as supply chain analysts.

Each mission presents delayed shipments, and the player must discover the true root-cause using analytics dashboards, anomaly indicators, and investigative tools.

**Technology goal:**
Showcase real-world analytics engineering, dashboards, and ML skills.

---

## 2️⃣ Primary Objectives

✔ Provide interactive investigation gameplay  
✔ Demonstrate real analytics workflows  
✔ Present business context & decision-making  
✔ Feature live dashboards & analysis tools  
✔ Optionally include ML-driven insights  
✔ Score the player based on accuracy  

---

## 3️⃣ Core Gameplay Loop

1. Load mission dataset
2. Player explores dashboards
3. Player filters/searches/inspects data
4. Player forms hypothesis
5. Player submits root-cause
6. System evaluates correctness
7. Score screen → next mission

---

## 4️⃣ User Actions Supported

### Data Interaction

- Filter shipments (supplier, warehouse, region, date)
- Inspect warehouse metrics
- Compare suppliers
- Analyze routes
- Review delay logs
- Visualize trends

### Decision Support

- Anomaly alerts
- Risk indicators
- KPI comparison
- Narrative clues

### Core Action

➡ **Submit final conclusion**

---

## 5️⃣ Data Sources

**Directory:** `/data`

**Files:**
- `shipments.csv`
- `warehouses.csv`
- `delays.csv`

**Minimal fields:**
- shipment_id
- warehouse_id
- supplier
- origin
- destination
- distance_km
- expected_time
- actual_time
- cost
- sku_count
- traffic_index

---

## 6️⃣ System Architecture

### High-Level Flow

```
CSV Data
→ Preprocessing (Pandas)
→ Analytics Engine
→ Visualization Layer
→ Game Logic Engine
→ Streamlit UI
→ Scoring System
→ Deployment
```

---

## 7️⃣ Component Blueprint

### Backend – Python

**`data_loader.py`**
- Loads CSVs + schema validation

**`preprocess.py`**
- Missing values
- Outlier removal
- Feature engineering:
  - transit_time
  - delay_flag
  - supplier_score

**`analysis_engine.py`**
- Metrics + KPIs

**`missions.py`**
- Mission config & correct answer

**`scoring.py`**
- Correctness
- Timing
- Hint penalty

**`ml/`**
- `anomaly_model.py` (IsolationForest)
- `delay_risk_model.py` (RandomForest)
- `forecasting.py` (Prophet/ARIMA)

### Frontend – Streamlit

**Home**
- Start game
- How to play
- About
- GitHub link

**Dashboard**
- KPI cards
- Charts
- Anomaly panel

**Investigation Mode**
- Filters
- Raw table
- Charts
- ML hints
- Narrative
- Submit guess

**Results**
- Correct vs incorrect
- Explanation
- Scores
- Next mission

---

## 8️⃣ KPIs Required

- Average delay
- Delay rate (%)
- Total shipments
- Late shipments
- Warehouse load score
- Supplier reliability score

---

## 9️⃣ Visualizations Needed

- Line charts
- Bar charts
- Bubble chart
- Scatter
- Geo route map (optional)

---

## 🔟 Machine Learning (Optional)

### Model 1: Delay Risk Predictor
- RandomForestRegressor
- Predicts minutes of delay

### Model 2: Anomaly Detector
- IsolationForest
- Flags abnormal shipments

### Model 3: SKU Forecaster
- Prophet/ARIMA
- Project future demand spikes

---

## 1️⃣1️⃣ Scoring System

**Factors:**
- Correctness
- Time taken
- Number of hints used
- Bonus rules allowed

---

## 1️⃣2️⃣ MVP Scope

**Must include:**
- 1 mission
- Dashboard
- Investigation mode
- Submit answer
- Score screen

**No ML required for MVP.**

---

## 1️⃣3️⃣ Tech Stack

- Python
- Pandas
- NumPy
- Scikit-Learn
- Streamlit
- Plotly
- Altair
- (optional) Prophet

**Deployment:** Streamlit Cloud

---

## 1️⃣4️⃣ Production Deployment Steps

1. Push repo to GitHub
2. Connect repo in Streamlit Cloud
3. Choose branch = main
4. App file = app.py
5. Deploy

---

## 1️⃣5️⃣ Roadmap

### v1 – MVP
- Dashboard
- 1 mission
- Scoring

### v2
- Anomaly ML
- Multiple missions

### v3
- Forecasting
- Mission tree
- Story mode

### v4
- Authentication
- Leaderboard

