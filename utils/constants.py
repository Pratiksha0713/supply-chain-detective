"""
Constants Module

Application-wide constants, configuration values, and enumerations
used throughout the Supply Chain Detective game.
"""

# File paths
DATA_DIR = "data"
SHIPMENTS_FILE = "shipments.csv"
WAREHOUSES_FILE = "warehouses.csv"
DELAYS_FILE = "delays.csv"

# Column names
SHIPMENT_ID = "shipment_id"
WAREHOUSE_ID = "warehouse_id"
SUPPLIER = "supplier"
ORIGIN = "origin"
DESTINATION = "destination"
DISTANCE_KM = "distance_km"
EXPECTED_TIME = "expected_time"
ACTUAL_TIME = "actual_time"
COST = "cost"
SKU_COUNT = "sku_count"
TRAFFIC_INDEX = "traffic_index"

# Game constants
MAX_HINTS = 3
BASE_SCORE = 1000
TIME_BONUS_THRESHOLD = 300  # seconds
HINT_PENALTY = 100

# UI constants
APP_TITLE = "🎮 Supply Chain Detective"
APP_ICON = "🎮"

# Mission types
MISSION_TYPES = ["supplier_issue", "warehouse_delay", "route_problem", "capacity_issue"]

# Scoring thresholds
SCORE_EXCELLENT = 900
SCORE_GOOD = 700
SCORE_AVERAGE = 500

