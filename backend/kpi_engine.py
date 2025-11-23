"""
KPI Engine Module

Calculates key performance indicators and metrics for supply chain analytics,
including delay rates, warehouse performance, and supplier reliability.
"""

import pandas as pd
import numpy as np
from typing import Dict, Union


def average_delay(df: pd.DataFrame) -> float:
    """
    Calculate average delay in minutes across all shipments.
    
    Delay is calculated as the difference between actual_time and expected_time.
    Only shipments with actual_time > expected_time are considered delayed.
    
    Args:
        df (pd.DataFrame): Shipments dataframe with 'expected_time' and 'actual_time' columns
        
    Returns:
        float: Average delay in minutes, or 0.0 if no delays exist
    """
    if df.empty or 'expected_time' not in df.columns or 'actual_time' not in df.columns:
        return 0.0
    
    # Calculate delay in minutes
    df_copy = df.copy()
    df_copy['delay_minutes'] = (df_copy['actual_time'] - df_copy['expected_time']).dt.total_seconds() / 60
    
    # Filter only delayed shipments (positive delays)
    delayed_shipments = df_copy[df_copy['delay_minutes'] > 0]
    
    if delayed_shipments.empty:
        return 0.0
    
    return float(delayed_shipments['delay_minutes'].mean())


def percent_delayed(df: pd.DataFrame) -> float:
    """
    Calculate percentage of delayed shipments.
    
    A shipment is considered delayed if actual_time > expected_time.
    
    Args:
        df (pd.DataFrame): Shipments dataframe with 'expected_time' and 'actual_time' columns
        
    Returns:
        float: Percentage of delayed shipments (0-100), or 0.0 if no data
    """
    if df.empty or 'expected_time' not in df.columns or 'actual_time' not in df.columns:
        return 0.0
    
    total_shipments = len(df)
    
    if total_shipments == 0:
        return 0.0
    
    # Count delayed shipments
    delayed_count = (df['actual_time'] > df['expected_time']).sum()
    
    return float((delayed_count / total_shipments) * 100)


def order_backlog(df: pd.DataFrame) -> int:
    """
    Calculate order backlog (count of pending/delayed orders).
    
    Orders are considered in backlog if they are delayed beyond expected delivery time.
    
    Args:
        df (pd.DataFrame): Shipments dataframe with 'expected_time' and 'actual_time' columns
        
    Returns:
        int: Count of orders in backlog
    """
    if df.empty or 'expected_time' not in df.columns or 'actual_time' not in df.columns:
        return 0
    
    # Count shipments where actual > expected
    backlog_count = (df['actual_time'] > df['expected_time']).sum()
    
    return int(backlog_count)


def warehouse_load_index(wh_df: pd.DataFrame) -> float:
    """
    Calculate warehouse load index (average utilization score).
    
    Load index is calculated as the ratio of current shipments to warehouse capacity.
    Returns average load score across all warehouses (0-100 scale).
    
    Args:
        wh_df (pd.DataFrame): Warehouse dataframe with 'capacity' and optionally 'current_load' columns
        
    Returns:
        float: Average warehouse load index (0-100), or 0.0 if no data
    """
    if wh_df.empty or 'capacity' not in wh_df.columns:
        return 0.0
    
    # If current_load exists, use it; otherwise estimate from shipments
    if 'current_load' in wh_df.columns:
        wh_df_copy = wh_df.copy()
        wh_df_copy['load_ratio'] = (wh_df_copy['current_load'] / wh_df_copy['capacity']) * 100
        wh_df_copy['load_ratio'] = wh_df_copy['load_ratio'].clip(0, 100)
        return float(wh_df_copy['load_ratio'].mean())
    else:
        # If no current_load, return capacity-based estimate
        # Assume 65% average utilization as baseline
        return 65.0


def supplier_reliability(df: pd.DataFrame) -> Dict[str, float]:
    """
    Calculate reliability score for each supplier.
    
    Reliability is calculated as: 100 - (delay_rate for that supplier)
    Higher scores indicate more reliable suppliers.
    
    Args:
        df (pd.DataFrame): Shipments dataframe with 'supplier', 'expected_time', and 'actual_time' columns
        
    Returns:
        Dict[str, float]: Dictionary mapping supplier names to reliability scores (0-100)
    """
    if df.empty or 'supplier' not in df.columns:
        return {}
    
    if 'expected_time' not in df.columns or 'actual_time' not in df.columns:
        return {}
    
    reliability_scores = {}
    
    # Group by supplier
    for supplier in df['supplier'].unique():
        supplier_df = df[df['supplier'] == supplier]
        
        total = len(supplier_df)
        if total == 0:
            continue
        
        # Calculate delay rate for this supplier
        delayed = (supplier_df['actual_time'] > supplier_df['expected_time']).sum()
        delay_rate = (delayed / total) * 100
        
        # Reliability is inverse of delay rate
        reliability = 100 - delay_rate
        reliability_scores[str(supplier)] = float(reliability)
    
    return reliability_scores


def cost_delay_correlation(df: pd.DataFrame) -> float:
    """
    Calculate correlation between shipment cost and delay.
    
    Measures the linear relationship between cost and delay time.
    Positive correlation suggests higher-cost shipments are more delayed.
    
    Args:
        df (pd.DataFrame): Shipments dataframe with 'cost', 'expected_time', and 'actual_time' columns
        
    Returns:
        float: Correlation coefficient (-1 to 1), or 0.0 if insufficient data
    """
    if df.empty or 'cost' not in df.columns:
        return 0.0
    
    if 'expected_time' not in df.columns or 'actual_time' not in df.columns:
        return 0.0
    
    # Calculate delay in minutes
    df_copy = df.copy()
    df_copy['delay_minutes'] = (df_copy['actual_time'] - df_copy['expected_time']).dt.total_seconds() / 60
    
    # Remove null values
    df_clean = df_copy[['cost', 'delay_minutes']].dropna()
    
    if len(df_clean) < 2:
        return 0.0
    
    # Calculate Pearson correlation
    correlation = df_clean['cost'].corr(df_clean['delay_minutes'])
    
    # Handle NaN result (e.g., if variance is zero)
    if pd.isna(correlation):
        return 0.0
    
    return float(correlation)


def calculate_total_shipments(df: pd.DataFrame) -> int:
    """
    Count total number of shipments.
    
    Args:
        df (pd.DataFrame): Shipments dataframe
        
    Returns:
        int: Total number of shipments
    """
    return len(df) if not df.empty else 0


def calculate_late_shipments(df: pd.DataFrame) -> int:
    """
    Count number of late shipments.
    
    Args:
        df (pd.DataFrame): Shipments dataframe with 'expected_time' and 'actual_time' columns
        
    Returns:
        int: Count of late shipments
    """
    return order_backlog(df)


def get_all_kpis(df: pd.DataFrame, wh_df: pd.DataFrame = None) -> Dict[str, Union[float, int, Dict]]:
    """
    Calculate and return all KPIs as dictionary.
    
    Args:
        df (pd.DataFrame): Shipments dataframe
        wh_df (pd.DataFrame, optional): Warehouses dataframe
        
    Returns:
        Dict: Dictionary containing all calculated KPIs
    """
    kpis = {
        'total_shipments': calculate_total_shipments(df),
        'late_shipments': calculate_late_shipments(df),
        'average_delay_minutes': round(average_delay(df), 2),
        'percent_delayed': round(percent_delayed(df), 2),
        'order_backlog': order_backlog(df),
        'cost_delay_correlation': round(cost_delay_correlation(df), 3),
        'supplier_reliability': supplier_reliability(df)
    }
    
    # Add warehouse load if warehouse data provided
    if wh_df is not None:
        kpis['warehouse_load_index'] = round(warehouse_load_index(wh_df), 2)
    
    return kpis

