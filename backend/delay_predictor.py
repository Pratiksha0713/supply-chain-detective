"""
Delay Prediction Model Module

Uses Random Forest Regressor to predict shipment delays based on
historical patterns and shipment characteristics.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from typing import Tuple, Dict, List
import logging

logger = logging.getLogger(__name__)

# Features used for delay prediction
PREDICTOR_FEATURES = ['distance_km', 'cost', 'sku_count', 'traffic_index']


def prepare_features(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Prepare feature matrix for delay prediction.
    
    Extracts features and calculates target variable (delay_minutes).
    
    Args:
        df (pd.DataFrame): Shipments dataframe with required columns
        
    Returns:
        Tuple[pd.DataFrame, pd.Series]: Feature matrix (X) and target vector (y)
        
    Raises:
        ValueError: If required columns are missing
    """
    required_cols = PREDICTOR_FEATURES + ['expected_time', 'actual_time']
    missing_cols = set(required_cols) - set(df.columns)
    
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")
    
    if df.empty:
        raise ValueError("Cannot prepare features from empty dataframe")
    
    # Calculate delay_minutes as target
    df_copy = df.copy()
    df_copy['delay_minutes'] = (df_copy['actual_time'] - df_copy['expected_time']).dt.total_seconds() / 60
    
    # Extract features
    X = df_copy[PREDICTOR_FEATURES].copy()
    y = df_copy['delay_minutes'].copy()
    
    # Handle missing values
    X = X.fillna(X.median())
    
    # Remove rows with missing target
    valid_idx = ~y.isna()
    X = X[valid_idx]
    y = y[valid_idx]
    
    return X, y


def train_delay_model(df: pd.DataFrame, test_size: float = 0.2, random_state: int = 42) -> Tuple[RandomForestRegressor, Dict[str, float]]:
    """
    Train Random Forest model to predict delay minutes.
    
    Uses distance_km, cost, sku_count, and traffic_index as features
    to predict shipment delay in minutes.
    
    Args:
        df (pd.DataFrame): Shipments dataframe with required features
        test_size (float): Proportion of data for testing (default: 0.2)
        random_state (int): Random seed for reproducibility (default: 42)
        
    Returns:
        Tuple[RandomForestRegressor, Dict[str, float]]: Trained model and performance metrics
        
    Raises:
        ValueError: If required features are missing or insufficient data
    """
    # Prepare features and target
    X, y = prepare_features(df)
    
    if len(X) < 10:
        raise ValueError(f"Insufficient data for training: only {len(X)} samples available")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    
    # Initialize and train Random Forest
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=random_state,
        n_jobs=-1  # Use all available cores
    )
    
    model.fit(X_train, y_train)
    
    # Evaluate on test set
    y_pred = model.predict(X_test)
    metrics = evaluate_model(y_test, y_pred)
    
    logger.info(f"✓ Trained delay prediction model on {len(X_train)} samples")
    logger.info(f"  MAE: {metrics['mae']:.2f} min, RMSE: {metrics['rmse']:.2f} min, R²: {metrics['r2']:.3f}")
    
    return model, metrics


def predict_delay(df: pd.DataFrame, model: RandomForestRegressor) -> pd.DataFrame:
    """
    Predict delay for shipments using trained model.
    
    Adds a new column 'predicted_delay' containing predicted delay in minutes.
    
    Args:
        df (pd.DataFrame): Shipments dataframe with required features
        model (RandomForestRegressor): Trained Random Forest model
        
    Returns:
        pd.DataFrame: Original dataframe with added predicted_delay column
        
    Raises:
        ValueError: If required features are missing
    """
    # Check for required features
    missing_features = set(PREDICTOR_FEATURES) - set(df.columns)
    if missing_features:
        raise ValueError(f"Missing required features: {missing_features}")
    
    if df.empty:
        df['predicted_delay'] = []
        return df
    
    # Prepare feature matrix
    X = df[PREDICTOR_FEATURES].copy()
    
    # Handle missing values (use same strategy as training)
    X = X.fillna(X.median())
    
    # Make predictions
    predictions = model.predict(X)
    
    # Add predictions to dataframe
    df_result = df.copy()
    df_result['predicted_delay'] = predictions
    
    # Log statistics
    avg_predicted = predictions.mean()
    logger.info(f"✓ Predicted delays for {len(df)} shipments (avg: {avg_predicted:.2f} min)")
    
    return df_result


def predict_delays(df: pd.DataFrame, model: RandomForestRegressor) -> pd.DataFrame:
    """
    Predict delay for shipments using trained model.
    
    Alias for predict_delay() function for backward compatibility.
    
    Args:
        df (pd.DataFrame): Shipments dataframe with required features
        model (RandomForestRegressor): Trained Random Forest model
        
    Returns:
        pd.DataFrame: Original dataframe with added predicted_delay column
    """
    return predict_delay(df, model)


def get_feature_importance(model: RandomForestRegressor) -> Dict[str, float]:
    """
    Get feature importance from trained model.
    
    Args:
        model (RandomForestRegressor): Trained Random Forest model
        
    Returns:
        Dict[str, float]: Dictionary mapping feature names to importance scores
    """
    if not hasattr(model, 'feature_importances_'):
        return {}
    
    importances = model.feature_importances_
    
    # Create dictionary of feature: importance
    feature_importance = {
        feature: float(importance)
        for feature, importance in zip(PREDICTOR_FEATURES, importances)
    }
    
    # Sort by importance (descending)
    feature_importance = dict(sorted(
        feature_importance.items(),
        key=lambda x: x[1],
        reverse=True
    ))
    
    return feature_importance


def evaluate_model(y_true: pd.Series, y_pred: np.ndarray) -> Dict[str, float]:
    """
    Evaluate model performance metrics.
    
    Calculates MAE, RMSE, and R² score.
    
    Args:
        y_true (pd.Series): True delay values
        y_pred (np.ndarray): Predicted delay values
        
    Returns:
        Dict[str, float]: Dictionary containing performance metrics
    """
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_true, y_pred)
    
    metrics = {
        'mae': round(float(mae), 2),
        'mse': round(float(mse), 2),
        'rmse': round(float(rmse), 2),
        'r2': round(float(r2), 4)
    }
    
    return metrics


def get_prediction_confidence(model: RandomForestRegressor, X: pd.DataFrame) -> np.ndarray:
    """
    Get prediction confidence intervals using ensemble variance.
    
    Args:
        model (RandomForestRegressor): Trained Random Forest model
        X (pd.DataFrame): Feature matrix
        
    Returns:
        np.ndarray: Standard deviation of predictions across trees
    """
    # Get predictions from each tree
    tree_predictions = np.array([tree.predict(X) for tree in model.estimators_])
    
    # Calculate standard deviation across trees
    std_predictions = np.std(tree_predictions, axis=0)
    
    return std_predictions

