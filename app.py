"""
Supply Chain Detective - Main Application Entry Point

Browser-based analytics puzzle game where players investigate
supply chain delays using data analysis and dashboards.
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import time
import sys

# Add paths for imports
sys.path.append('backend')
sys.path.append('frontend')

# Backend imports
from missions import get_mission, get_mission_count, get_mission_hints, get_correct_answer
from scoring import score_submission
from data_loader import load_shipment_data, load_warehouse_data
from kpi_engine import calculate_kpis

# Frontend imports
from components import apply_custom_styling, render_header, mission_header, submit_button, alert_box
from dashboard_ui import render_dashboard
from investigation_ui import render_investigation
from results_ui import render_results


def initialize_session_state():
    """Initialize Streamlit session state variables."""
    # Screen navigation
    if 'screen' not in st.session_state:
        st.session_state.screen = 'home'
    
    # Mission tracking
    if 'mission_index' not in st.session_state:
        st.session_state.mission_index = 0
    
    # Timer for scoring
    if 'timer_start' not in st.session_state:
        st.session_state.timer_start = None
    
    # Hints tracking
    if 'hints_used' not in st.session_state:
        st.session_state.hints_used = 0
    
    # User submission
    if 'user_guess' not in st.session_state:
        st.session_state.user_guess = ''
    
    # Score tracking
    if 'final_score' not in st.session_state:
        st.session_state.final_score = 0
    
    if 'score_breakdown' not in st.session_state:
        st.session_state.score_breakdown = {}
    
    # Mission data cache
    if 'current_mission' not in st.session_state:
        st.session_state.current_mission = None
    
    if 'mission_data' not in st.session_state:
        st.session_state.mission_data = None


def load_mission_data(mission_index):
    """Load data for the current mission."""
    try:
        # Generate sample data for the mission
        np.random.seed(mission_index + 42)
        
        # Sample shipment data
        n_records = 200
        dates = pd.date_range(start='2024-01-01', periods=n_records, freq='D')
        
        shipment_df = pd.DataFrame({
            'shipment_id': range(1, n_records + 1),
            'supplier': np.random.choice(['Supplier A', 'Supplier B', 'Supplier C', 'Supplier D'], n_records),
            'warehouse_id': np.random.choice(['WH-001', 'WH-002', 'WH-003'], n_records),
            'region': np.random.choice(['North', 'South', 'East', 'West'], n_records),
            'date': dates,
            'delay_days': np.random.exponential(2 + mission_index, n_records),
            'cost': np.random.uniform(1000, 15000, n_records),
            'quantity': np.random.randint(10, 500, n_records),
            'anomaly': np.random.choice([0, 1], n_records, p=[0.85, 0.15])
        })
        
        # Warehouse data
        warehouse_df = pd.DataFrame({
            'warehouse_id': ['WH-001', 'WH-002', 'WH-003'],
            'capacity': [1000, 1500, 800],
            'utilization': [0.85, 0.92, 0.78]
        })
        
        # Delay data (same as shipment for simplicity)
        delay_df = shipment_df[['shipment_id', 'date', 'delay_days', 'supplier']].copy()
        
        # Anomaly data
        anomaly_df = shipment_df[shipment_df['anomaly'] == 1].copy()
        
        return shipment_df, warehouse_df, delay_df, anomaly_df
    
    except Exception as e:
        st.error(f"Error loading mission data: {str(e)}")
        return None, None, None, None


def render_home_page():
    """Render home page with game introduction."""
    render_header()
    
    st.markdown("## Welcome, Detective! 🕵️")
    
    st.markdown("""
        ### Your Mission
        
        You are a **Supply Chain Detective**, tasked with investigating mysterious disruptions 
        in global supply chains. Use your analytical skills to:
        
        - 📊 Analyze supply chain data and KPIs
        - 🔍 Investigate anomalies and patterns
        - 🤖 Leverage ML insights for predictions
        - 🎯 Identify root causes of supply chain issues
        
        ### How It Works
        
        1. **Dashboard**: Review key metrics and identify problems
        2. **Investigation Mode**: Filter data, analyze patterns, and use hints
        3. **Submit**: Propose your root cause analysis
        4. **Results**: See your score and learn from feedback
        
        ### Scoring System
        
        - ✅ **Correct Answer**: 100 points base score
        - ⏱️ **Time Penalty**: -0.1 points per second
        - 💡 **Hint Penalty**: -10 points per hint used
        
        The faster and more independently you solve the case, the higher your score!
    """)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if submit_button("🎮 Start Playing"):
            st.session_state.screen = 'dashboard'
            st.session_state.mission_index = 0
            st.rerun()
    
    st.markdown("---")
    
    # Mission preview
    st.markdown("### 🎯 Available Missions")
    mission_count = get_mission_count()
    
    for i in range(mission_count):
        mission = get_mission(i)
        if mission:
            with st.expander(f"Mission {i+1}: {mission['title']} - {mission['difficulty']}"):
                st.write(mission['description'])


def render_dashboard_screen():
    """Render dashboard screen with mission overview."""
    # Load current mission
    mission = get_mission(st.session_state.mission_index)
    st.session_state.current_mission = mission
    
    if not mission:
        st.error("Mission not found!")
        return
    
    # Show mission header
    mission_header(f"Mission {st.session_state.mission_index + 1}: {mission['title']}")
    
    # Load mission data
    if st.session_state.mission_data is None:
        sh_df, wh_df, delay_df, anomaly_df = load_mission_data(st.session_state.mission_index)
        st.session_state.mission_data = (sh_df, wh_df, delay_df, anomaly_df)
    else:
        sh_df, wh_df, delay_df, anomaly_df = st.session_state.mission_data
    
    # Render dashboard
    if sh_df is not None:
        render_dashboard(sh_df, wh_df, delay_df, anomaly_df)
    
    st.markdown("---")
    
    # Button to start investigation
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if submit_button("🔍 Start Investigation"):
            st.session_state.screen = 'investigation'
            st.session_state.timer_start = time.time()
            st.session_state.hints_used = 0
            st.rerun()


def render_investigation_screen():
    """Render investigation mode screen."""
    # Get current mission and data
    mission = st.session_state.current_mission
    
    if not mission:
        st.error("Mission not loaded!")
        return
    
    sh_df, wh_df, delay_df, anomaly_df = st.session_state.mission_data
    
    # Prepare ML insights
    ml_insights = {
        'delay_prediction': delay_df['delay_days'].mean() if delay_df is not None else 0,
        'anomaly_count': len(anomaly_df) if anomaly_df is not None else 0,
        'risk_factors': {
            'supplier_reliability': 0.75,
            'warehouse_capacity': 0.68,
            'seasonal_demand': 0.82
        }
    }
    
    # Get hints
    hints = get_mission_hints(mission['id'])
    
    # Render investigation UI
    filtered_df, user_conclusion, submit_clicked = render_investigation(
        df=sh_df,
        mission=mission,
        ml_insights=ml_insights,
        hints=hints
    )
    
    # Handle submission
    if submit_clicked:
        if not user_conclusion or len(user_conclusion.strip()) < 10:
            alert_box("Please enter a more detailed conclusion (at least 10 characters).")
        else:
            # Calculate time taken
            if st.session_state.timer_start:
                time_taken = time.time() - st.session_state.timer_start
            else:
                time_taken = 0
            
            # Get correct answer
            correct_answer = get_correct_answer(mission['id'])
            
            # Calculate score
            final_score, breakdown = score_submission(
                user_guess=user_conclusion,
                correct_cause=correct_answer,
                time_taken=time_taken,
                hints_used=st.session_state.hints_used
            )
            
            # Store results
            st.session_state.user_guess = user_conclusion
            st.session_state.final_score = final_score
            st.session_state.score_breakdown = breakdown
            
            # Move to results screen
            st.session_state.screen = 'results'
            st.rerun()


def render_results_screen():
    """Render results screen with score and feedback."""
    # Get stored results
    final_score = st.session_state.final_score
    user_guess = st.session_state.user_guess
    score_breakdown = st.session_state.score_breakdown
    
    # Get correct answer
    mission = st.session_state.current_mission
    correct_answer = get_correct_answer(mission['id']) if mission else "Unknown"
    
    # Render results
    next_mission_clicked = render_results(
        final_score=final_score,
        user_guess=user_guess,
        correct_cause=correct_answer,
        score_breakdown=score_breakdown
    )
    
    # Handle next mission button
    if next_mission_clicked:
        # Move to next mission
        st.session_state.mission_index += 1
        
        # Check if there are more missions
        if st.session_state.mission_index >= get_mission_count():
            st.session_state.mission_index = 0  # Loop back to first mission
        
        # Reset state for next mission
        st.session_state.screen = 'dashboard'
        st.session_state.mission_data = None
        st.session_state.current_mission = None
        st.session_state.timer_start = None
        st.session_state.hints_used = 0
        st.session_state.user_guess = ''
        
        st.rerun()
    
    # Handle retry or return to dashboard
    if st.session_state.get('retry_mission', False):
        st.session_state.screen = 'investigation'
        st.session_state.timer_start = time.time()
        st.session_state.hints_used = 0
        st.session_state.retry_mission = False
        st.rerun()
    
    if st.session_state.get('return_to_dashboard', False):
        st.session_state.screen = 'dashboard'
        st.session_state.return_to_dashboard = False
        st.rerun()


def render_sidebar():
    """Render sidebar with navigation and game info."""
    with st.sidebar:
        st.markdown("### 🎮 Supply Chain Detective")
        st.markdown("---")
        
        # Show current screen
        st.markdown(f"**Current Screen:** {st.session_state.screen.title()}")
        
        # Show mission info if in game
        if st.session_state.screen != 'home':
            mission = st.session_state.current_mission
            if mission:
                st.markdown(f"**Mission:** {st.session_state.mission_index + 1}/{get_mission_count()}")
                st.markdown(f"**Difficulty:** {mission.get('difficulty', 'N/A')}")
        
        # Show timer if in investigation mode
        if st.session_state.screen == 'investigation' and st.session_state.timer_start:
            elapsed = int(time.time() - st.session_state.timer_start)
            minutes = elapsed // 60
            seconds = elapsed % 60
            st.markdown(f"**Time:** {minutes:02d}:{seconds:02d}")
        
        # Show hints used
        if st.session_state.screen == 'investigation':
            st.markdown(f"**Hints Used:** {st.session_state.hints_used}")
        
        st.markdown("---")
        
        # Navigation buttons
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.screen = 'home'
            st.rerun()
        
        if st.session_state.screen != 'home':
            if st.button("📊 Dashboard", use_container_width=True):
                st.session_state.screen = 'dashboard'
                st.rerun()


def main():
    """Main application entry point."""
    st.set_page_config(
        page_title="Supply Chain Detective",
        page_icon="🕵️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Apply custom styling
    apply_custom_styling()
    
    # Initialize session state
    initialize_session_state()
    
    # Render sidebar
    render_sidebar()
    
    # Route to appropriate screen
    if st.session_state.screen == 'home':
        render_home_page()
    
    elif st.session_state.screen == 'dashboard':
        render_dashboard_screen()
    
    elif st.session_state.screen == 'investigation':
        render_investigation_screen()
    
    elif st.session_state.screen == 'results':
        render_results_screen()
    
    else:
        st.error(f"Unknown screen: {st.session_state.screen}")


if __name__ == "__main__":
    main()

