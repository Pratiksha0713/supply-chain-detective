"""
Data Loader Module

Responsible for loading CSV files from the /data directory and performing
schema validation to ensure data integrity before processing.
"""

import pandas as pd
import streamlit as st
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Data directory path
DATA_DIR = Path("data")


@st.cache_data
def load_shipments():
    """
    Load shipments.csv and validate schema.
    
    Returns:
        pd.DataFrame: Shipments data with validated types
    """
    try:
        filepath = DATA_DIR / "shipments.csv"
        
        # Load CSV
        df = pd.read_csv(filepath)
        
        # Validate required columns
        required_columns = [
            'shipment_id', 'warehouse_id', 'supplier', 'origin', 
            'destination', 'distance_km', 'expected_time', 
            'actual_time', 'cost', 'sku_count', 'traffic_index'
        ]
        
        missing_columns = set(required_columns) - set(df.columns)
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
        
        # Type conversions and validation
        df['shipment_id'] = df['shipment_id'].astype(str)
        df['warehouse_id'] = df['warehouse_id'].astype(str)
        df['supplier'] = df['supplier'].astype(str)
        df['origin'] = df['origin'].astype(str)
        df['destination'] = df['destination'].astype(str)
        
        # Numeric columns
        df['distance_km'] = pd.to_numeric(df['distance_km'], errors='coerce')
        df['cost'] = pd.to_numeric(df['cost'], errors='coerce')
        df['sku_count'] = pd.to_numeric(df['sku_count'], errors='coerce')
        df['traffic_index'] = pd.to_numeric(df['traffic_index'], errors='coerce')
        
        # DateTime columns
        df['expected_time'] = pd.to_datetime(df['expected_time'], errors='coerce')
        df['actual_time'] = pd.to_datetime(df['actual_time'], errors='coerce')
        
        # Log success
        logger.info(f"✓ Loaded {len(df)} shipments from {filepath}")
        
        return df
        
    except FileNotFoundError:
        logger.error(f"✗ File not found: {filepath}")
        st.error(f"Could not find file: {filepath}")
        return pd.DataFrame()
    except Exception as e:
        logger.error(f"✗ Error loading shipments: {str(e)}")
        st.error(f"Error loading shipments: {str(e)}")
        return pd.DataFrame()


@st.cache_data
def load_warehouses():
    """
    Load warehouses.csv and validate schema.
    
    Returns:
        pd.DataFrame: Warehouses data with validated types
    """
    try:
        filepath = DATA_DIR / "warehouses.csv"
        
        # Load CSV
        df = pd.read_csv(filepath)
        
        # Validate required columns
        required_columns = ['warehouse_id', 'warehouse_name', 'location', 'capacity']
        
        missing_columns = set(required_columns) - set(df.columns)
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
        
        # Type conversions and validation
        df['warehouse_id'] = df['warehouse_id'].astype(str)
        df['warehouse_name'] = df['warehouse_name'].astype(str)
        df['location'] = df['location'].astype(str)
        df['capacity'] = pd.to_numeric(df['capacity'], errors='coerce')
        
        # Log success
        logger.info(f"✓ Loaded {len(df)} warehouses from {filepath}")
        
        return df
        
    except FileNotFoundError:
        logger.error(f"✗ File not found: {filepath}")
        st.error(f"Could not find file: {filepath}")
        return pd.DataFrame()
    except Exception as e:
        logger.error(f"✗ Error loading warehouses: {str(e)}")
        st.error(f"Error loading warehouses: {str(e)}")
        return pd.DataFrame()


@st.cache_data
def load_delays():
    """
    Load delays.csv and validate schema.
    
    Returns:
        pd.DataFrame: Delays data with validated types
    """
    try:
        filepath = DATA_DIR / "delays.csv"
        
        # Load CSV
        df = pd.read_csv(filepath)
        
        # Validate required columns
        required_columns = [
            'shipment_id', 'delay_minutes', 'delay_category', 
            'reported_reason', 'timestamp'
        ]
        
        missing_columns = set(required_columns) - set(df.columns)
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
        
        # Type conversions and validation
        df['shipment_id'] = df['shipment_id'].astype(str)
        df['delay_minutes'] = pd.to_numeric(df['delay_minutes'], errors='coerce')
        df['delay_category'] = df['delay_category'].astype(str)
        df['reported_reason'] = df['reported_reason'].astype(str)
        
        # DateTime column
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
        
        # Log success
        logger.info(f"✓ Loaded {len(df)} delay records from {filepath}")
        
        return df
        
    except FileNotFoundError:
        logger.error(f"✗ File not found: {filepath}")
        st.error(f"Could not find file: {filepath}")
        return pd.DataFrame()
    except Exception as e:
        logger.error(f"✗ Error loading delays: {str(e)}")
        st.error(f"Error loading delays: {str(e)}")
        return pd.DataFrame()


def validate_schema(df, expected_columns):
    """
    Validate that dataframe contains expected columns.
    
    Args:
        df (pd.DataFrame): DataFrame to validate
        expected_columns (list): List of expected column names
        
    Returns:
        bool: True if schema is valid, False otherwise
    """
    if df.empty:
        return False
    
    missing_columns = set(expected_columns) - set(df.columns)
    
    if missing_columns:
        logger.warning(f"Missing columns: {missing_columns}")
        return False
    
    return True


def load_all_data():
    """
    Load all CSV files and return as dictionary of dataframes.
    
    Returns:
        dict: Dictionary with keys 'shipments', 'warehouses', 'delays'
    """
    logger.info("Loading all datasets...")
    
    data = {
        'shipments': load_shipments(),
        'warehouses': load_warehouses(),
        'delays': load_delays()
    }
    
    # Log summary
    total_rows = sum(len(df) for df in data.values())
    logger.info(f"✓ Total records loaded: {total_rows}")
    
    return data

