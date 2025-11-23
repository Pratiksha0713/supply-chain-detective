"""
Anomaly Detection Model Module

Uses Isolation Forest algorithm to detect anomalous shipments
that deviate from normal supply chain patterns.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from typing import Tuple, Dict, Optional
import logging

logger = logging.getLogger(__name__)

# Features used for anomaly detection
ANOMALY_FEATURES = ['delay_minutes', 'distance_km', 'cost']


def train_anomaly_model(df: pd.DataFrame, contamination: float = 0.1, random_state: int = 42) -> IsolationForest:
    """
    Train Isolation Forest model on shipment data.
    
    Uses delay_minutes, distance_km, and cost as features to identify
    anomalous shipments that deviate from normal patterns.
    
    Args:
        df (pd.DataFrame): Shipments dataframe with required features
        contamination (float): Proportion of outliers in dataset (default: 0.1)
        random_state (int): Random seed for reproducibility (default: 42)
        
    Returns:
        IsolationForest: Trained anomaly detection model
        
    Raises:
        ValueError: If required features are missing from dataframe
    """
    # Check for required features
    missing_features = set(ANOMALY_FEATURES) - set(df.columns)
    if missing_features:
        raise ValueError(f"Missing required features: {missing_features}")
    
    if df.empty:
        raise ValueError("Cannot train model on empty dataframe")
    
    # Prepare feature matrix
    X = df[ANOMALY_FEATURES].copy()
    
    # Handle missing values
    X = X.fillna(X.median())
    
    # Check for sufficient data
    if len(X) < 10:
        logger.warning(f"Training on only {len(X)} samples - results may be unreliable")
    
    # Initialize and train Isolation Forest
    model = IsolationForest(
        contamination=contamination,
        random_state=random_state,
        n_estimators=100,
        max_samples='auto',
        n_jobs=-1  # Use all available cores
    )
    
    model.fit(X)
    
    logger.info(f"✓ Trained anomaly detection model on {len(X)} samples")
    
    return model


def detect_anomalies(df: pd.DataFrame, model: IsolationForest) -> pd.DataFrame:
    """
    Detect anomalies in shipment data using trained model.
    
    Adds two columns to the dataframe:
    - anomaly_flag: Boolean indicating if shipment is anomalous (True = anomaly)
    - anomaly_score: Anomaly score (lower = more anomalous)
    
    Args:
        df (pd.DataFrame): Shipments dataframe with required features
        model (IsolationForest): Trained Isolation Forest model
        
    Returns:
        pd.DataFrame: Original dataframe with added anomaly_flag and anomaly_score columns
        
    Raises:
        ValueError: If required features are missing from dataframe
    """
    # Check for required features
    missing_features = set(ANOMALY_FEATURES) - set(df.columns)
    if missing_features:
        raise ValueError(f"Missing required features: {missing_features}")
    
    if df.empty:
        df['anomaly_flag'] = []
        df['anomaly_score'] = []
        return df
    
    # Prepare feature matrix
    X = df[ANOMALY_FEATURES].copy()
    
    # Handle missing values (use same strategy as training)
    X = X.fillna(X.median())
    
    # Predict anomalies (-1 = anomaly, 1 = normal)
    predictions = model.predict(X)
    
    # Get anomaly scores (lower scores = more anomalous)
    scores = model.score_samples(X)
    
    # Add results to dataframe
    df_result = df.copy()
    df_result['anomaly_flag'] = (predictions == -1)
    df_result['anomaly_score'] = scores
    
    # Log results
    anomaly_count = df_result['anomaly_flag'].sum()
    anomaly_pct = (anomaly_count / len(df_result)) * 100
    logger.info(f"✓ Detected {anomaly_count} anomalies ({anomaly_pct:.1f}%)")
    
    return df_result


def get_anomaly_scores(df: pd.DataFrame, model: IsolationForest) -> np.ndarray:
    """
    Get anomaly scores for each shipment.
    
    Lower scores indicate more anomalous behavior.
    
    Args:
        df (pd.DataFrame): Shipments dataframe with required features
        model (IsolationForest): Trained Isolation Forest model
        
    Returns:
        np.ndarray: Array of anomaly scores
    """
    if df.empty:
        return np.array([])
    
    # Prepare feature matrix
    X = df[ANOMALY_FEATURES].copy()
    X = X.fillna(X.median())
    
    # Get anomaly scores
    scores = model.score_samples(X)
    
    return scores


def flag_anomalous_shipments(df: pd.DataFrame, threshold_percentile: float = 10) -> pd.DataFrame:
    """
    Flag shipments identified as anomalies based on threshold.
    
    Alternative method that doesn't require pre-trained model.
    Flags bottom N% of scores as anomalies.
    
    Args:
        df (pd.DataFrame): Dataframe with anomaly_score column
        threshold_percentile (float): Percentile threshold for flagging (default: 10)
        
    Returns:
        pd.DataFrame: Dataframe with updated anomaly_flag column
    """
    if df.empty or 'anomaly_score' not in df.columns:
        return df
    
    df_result = df.copy()
    
    # Calculate threshold
    threshold = np.percentile(df['anomaly_score'], threshold_percentile)
    
    # Flag anomalies
    df_result['anomaly_flag'] = df_result['anomaly_score'] < threshold
    
    return df_result


def get_anomaly_insights(df: pd.DataFrame) -> Dict[str, any]:
    """
    Generate insights about detected anomalies.
    
    Args:
        df (pd.DataFrame): Dataframe with anomaly_flag column and features
        
    Returns:
        Dict: Dictionary containing anomaly insights and statistics
    """
    if df.empty or 'anomaly_flag' not in df.columns:
        return {
            'total_anomalies': 0,
            'anomaly_percentage': 0.0,
            'insights': []
        }
    
    anomalies = df[df['anomaly_flag'] == True]
    normal = df[df['anomaly_flag'] == False]
    
    insights = {
        'total_anomalies': len(anomalies),
        'anomaly_percentage': (len(anomalies) / len(df)) * 100 if len(df) > 0 else 0.0,
        'insights': []
    }
    
    # Compare anomalies to normal shipments
    if not anomalies.empty and not normal.empty:
        for feature in ANOMALY_FEATURES:
            if feature in df.columns:
                anom_mean = anomalies[feature].mean()
                normal_mean = normal[feature].mean()
                diff_pct = ((anom_mean - normal_mean) / normal_mean * 100) if normal_mean != 0 else 0
                
                insights['insights'].append({
                    'feature': feature,
                    'anomaly_avg': round(anom_mean, 2),
                    'normal_avg': round(normal_mean, 2),
                    'difference_pct': round(diff_pct, 2)
                })
    
    # Add most anomalous shipments
    if 'anomaly_score' in df.columns and not anomalies.empty:
        most_anomalous = anomalies.nsmallest(5, 'anomaly_score')
        if 'shipment_id' in df.columns:
            insights['most_anomalous_ids'] = most_anomalous['shipment_id'].tolist()
    
    return insights

