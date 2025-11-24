"""
Investigation UI Module

Investigation mode interface with filters, data tables, charts,
and tools for player to analyze supply chain issues.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
sys.path.append('frontend')

from components import mission_header, alert_box, submit_button, render_info_box


def render_investigation(df, mission, ml_insights=None, hints=None):
    """
    Render complete investigation interface with filters, data, and submission form.
    
    Args:
        df (pd.DataFrame): The full dataset to investigate
        mission (dict): Mission details (title, description, hints)
        ml_insights (dict, optional): ML model predictions and insights
        hints (list, optional): Available hints for the mission
        
    Returns:
        tuple: (filtered_df, user_conclusion, submit_clicked)
    """
    # Mission header
    if mission and 'title' in mission:
        mission_header(mission['title'])
    else:
        mission_header("Investigation Mode")
    
    # Create main layout: left panel (filters) and right panel (content)
    left_col, right_col = st.columns([1, 2])
    
    # LEFT PANEL: Filters
    with left_col:
        st.markdown("### 🔍 Filters")
        filtered_df = render_filter_panel(df)
    
    # RIGHT PANEL: Mission description, data, and insights
    with right_col:
        # Mission description
        if mission and 'description' in mission:
            render_narrative_section(mission)
        
        # Raw data table
        st.markdown("### 📊 Data Explorer")
        render_shipment_table(filtered_df)
        
        # ML insights
        if ml_insights:
            st.markdown("### 🤖 ML Insights")
            render_ml_insights_panel(ml_insights)
        
        # Hints section
        if hints:
            render_ml_hints(hints)
    
    # BOTTOM: Conclusion submission form
    st.markdown("---")
    st.markdown("### 📝 Submit Your Conclusion")
    user_conclusion, submit_clicked = render_submit_form()
    
    return filtered_df, user_conclusion, submit_clicked


def render_filter_panel(df):
    """
    Render filter controls for data exploration in the left panel.
    
    Args:
        df (pd.DataFrame): The dataset to filter
        
    Returns:
        pd.DataFrame: Filtered dataframe based on user selections
    """
    if df is None or df.empty:
        st.warning("No data available to filter.")
        return df
    
    st.markdown("#### Filter Options")
    
    filtered_df = df.copy()
    
    # Supplier filter
    if 'supplier' in df.columns:
        suppliers = ['All'] + sorted(df['supplier'].unique().tolist())
        selected_supplier = st.selectbox("🏭 Supplier", suppliers, key="supplier_filter")
        
        if selected_supplier != 'All':
            filtered_df = filtered_df[filtered_df['supplier'] == selected_supplier]
    
    # Warehouse filter
    if 'warehouse_id' in df.columns or 'warehouse' in df.columns:
        warehouse_col = 'warehouse_id' if 'warehouse_id' in df.columns else 'warehouse'
        warehouses = ['All'] + sorted(df[warehouse_col].unique().tolist())
        selected_warehouse = st.selectbox("🏢 Warehouse", warehouses, key="warehouse_filter")
        
        if selected_warehouse != 'All':
            filtered_df = filtered_df[filtered_df[warehouse_col] == selected_warehouse]
    
    # Region filter
    if 'region' in df.columns:
        regions = ['All'] + sorted(df['region'].unique().tolist())
        selected_region = st.selectbox("🌍 Region", regions, key="region_filter")
        
        if selected_region != 'All':
            filtered_df = filtered_df[filtered_df['region'] == selected_region]
    
    # Date range filter
    date_col = None
    for col in ['date', 'ship_date', 'delivery_date', 'timestamp']:
        if col in df.columns:
            date_col = col
            break
    
    if date_col:
        st.markdown("📅 **Date Range**")
        
        # Convert to datetime if not already
        if not pd.api.types.is_datetime64_any_dtype(df[date_col]):
            filtered_df[date_col] = pd.to_datetime(filtered_df[date_col], errors='coerce')
        
        min_date = filtered_df[date_col].min()
        max_date = filtered_df[date_col].max()
        
        if pd.notna(min_date) and pd.notna(max_date):
            date_range = st.date_input(
                "Select date range",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date,
                key="date_range_filter"
            )
            
            if len(date_range) == 2:
                start_date, end_date = date_range
                filtered_df = filtered_df[
                    (filtered_df[date_col].dt.date >= start_date) &
                    (filtered_df[date_col].dt.date <= end_date)
                ]
    
    # Anomalies only toggle
    if 'anomaly' in df.columns or 'is_anomaly' in df.columns:
        anomaly_col = 'anomaly' if 'anomaly' in df.columns else 'is_anomaly'
        show_anomalies_only = st.checkbox("⚠️ Show Anomalies Only", value=False, key="anomaly_filter")
        
        if show_anomalies_only:
            filtered_df = filtered_df[filtered_df[anomaly_col] == 1]
    
    # Display filter summary
    st.markdown("---")
    st.markdown("#### 📊 Filter Summary")
    st.metric("Records Shown", f"{len(filtered_df):,}")
    st.metric("Total Records", f"{len(df):,}")
    
    if len(filtered_df) < len(df):
        percentage = (len(filtered_df) / len(df)) * 100
        st.info(f"Showing {percentage:.1f}% of data")
    
    return filtered_df


def render_shipment_table(df):
    """
    Render interactive table of shipment data.
    
    Args:
        df (pd.DataFrame): Filtered dataframe to display
    """
    if df is None or df.empty:
        st.warning("No data to display with current filters.")
        return
    
    # Show table statistics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Records", len(df))
    
    with col2:
        if 'delay_days' in df.columns:
            avg_delay = df['delay_days'].mean()
            st.metric("Avg Delay", f"{avg_delay:.1f} days")
    
    with col3:
        if 'cost' in df.columns:
            total_cost = df['cost'].sum()
            st.metric("Total Cost", f"${total_cost/1000:.1f}K")
    
    # Table display options
    display_mode = st.radio(
        "Display Mode",
        ["Summary View", "Detailed View"],
        horizontal=True,
        key="table_display_mode"
    )
    
    if display_mode == "Summary View":
        # Show limited columns
        summary_cols = []
        for col in ['shipment_id', 'supplier', 'warehouse_id', 'delay_days', 'cost', 'anomaly']:
            if col in df.columns:
                summary_cols.append(col)
        
        if summary_cols:
            display_df = df[summary_cols].head(100)
        else:
            display_df = df.head(100)
    else:
        display_df = df.head(100)
    
    # Display the table
    st.dataframe(
        display_df,
        use_container_width=True,
        height=400
    )
    
    if len(df) > 100:
        st.info(f"Showing first 100 of {len(df)} records")
    
    # Download option
    csv = df.to_csv(index=False)
    st.download_button(
        label="📥 Download Filtered Data (CSV)",
        data=csv,
        file_name="filtered_supply_chain_data.csv",
        mime="text/csv"
    )


def render_ml_insights_panel(ml_insights):
    """
    Render ML-powered insights panel.
    
    Args:
        ml_insights (dict): Dictionary containing ML predictions and insights
    """
    if not ml_insights:
        st.info("No ML insights available yet.")
        return
    
    # Display delay predictions if available
    if 'delay_prediction' in ml_insights:
        render_info_box(
            f"🤖 Delay Prediction Model: Expected delay of {ml_insights['delay_prediction']:.1f} days for high-risk shipments.",
            type="info"
        )
    
    # Display anomaly detection results
    if 'anomaly_count' in ml_insights:
        anomaly_count = ml_insights['anomaly_count']
        if anomaly_count > 0:
            render_info_box(
                f"⚠️ Anomaly Detection: {anomaly_count} unusual patterns detected in the data.",
                type="warning"
            )
        else:
            render_info_box(
                "✅ Anomaly Detection: No significant anomalies detected.",
                type="success"
            )
    
    # Display top risk factors
    if 'risk_factors' in ml_insights:
        st.markdown("#### 🎯 Top Risk Factors")
        risk_factors = ml_insights['risk_factors']
        
        for i, (factor, score) in enumerate(risk_factors.items(), 1):
            st.write(f"{i}. **{factor.replace('_', ' ').title()}**: {score:.2f}")
    
    # Display feature importance if available
    if 'feature_importance' in ml_insights:
        st.markdown("#### 📊 Feature Importance")
        
        importance_df = pd.DataFrame(
            list(ml_insights['feature_importance'].items()),
            columns=['Feature', 'Importance']
        ).sort_values('Importance', ascending=False)
        
        fig = px.bar(
            importance_df.head(10),
            x='Importance',
            y='Feature',
            orientation='h',
            color='Importance',
            color_continuous_scale='Blues'
        )
        
        fig.update_layout(
            height=300,
            margin=dict(l=0, r=0, t=10, b=0),
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)


def render_analysis_charts(df):
    """
    Render charts for detailed data analysis.
    
    Args:
        df (pd.DataFrame): Data to visualize
    """
    if df is None or df.empty:
        st.info("No data available for visualization.")
        return
    
    st.markdown("### 📈 Analysis Charts")
    
    # Create tabs for different chart types
    tab1, tab2, tab3 = st.tabs(["Distribution", "Trends", "Correlations"])
    
    with tab1:
        if 'delay_days' in df.columns:
            fig = px.histogram(
                df,
                x='delay_days',
                nbins=30,
                title="Delay Distribution",
                labels={'delay_days': 'Delay (days)', 'count': 'Frequency'}
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        date_col = None
        for col in ['date', 'ship_date', 'delivery_date']:
            if col in df.columns:
                date_col = col
                break
        
        if date_col and 'delay_days' in df.columns:
            fig = px.line(
                df.sort_values(date_col),
                x=date_col,
                y='delay_days',
                title="Delay Trend Over Time"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
        if len(numeric_cols) >= 2:
            correlation_matrix = df[numeric_cols].corr()
            fig = px.imshow(
                correlation_matrix,
                text_auto=True,
                aspect="auto",
                title="Correlation Matrix"
            )
            st.plotly_chart(fig, use_container_width=True)


def render_ml_hints(hints):
    """
    Render ML-powered hint panel.
    
    Args:
        hints (list): List of available hints
    """
    if not hints:
        return
    
    st.markdown("### 💡 Hints Available")
    
    # Initialize hints used counter in session state
    if 'hints_used' not in st.session_state:
        st.session_state.hints_used = 0
    
    st.info(f"Hints used: {st.session_state.hints_used}/{len(hints)} (Each hint costs 10 points)")
    
    # Show hints in expandable sections
    for i, hint in enumerate(hints, 1):
        hint_key = f"hint_{i}"
        
        if hint_key not in st.session_state:
            st.session_state[hint_key] = False
        
        if st.session_state[hint_key]:
            # Hint already revealed
            with st.expander(f"💡 Hint {i}", expanded=False):
                st.write(hint)
        else:
            # Hint not yet revealed
            if st.button(f"🔓 Reveal Hint {i} (-10 points)", key=f"reveal_{hint_key}"):
                st.session_state[hint_key] = True
                st.session_state.hints_used += 1
                st.rerun()


def render_narrative_section(mission):
    """
    Render mission narrative and context.
    
    Args:
        mission (dict): Mission details including description
    """
    st.markdown("### 📖 Mission Brief")
    
    with st.container():
        st.markdown(f"""
            <div style="
                background-color: #f8f9fa;
                padding: 20px;
                border-radius: 10px;
                border-left: 5px solid #667eea;
                margin: 10px 0;
            ">
                <p style="
                    color: #333;
                    font-size: 16px;
                    line-height: 1.6;
                    margin: 0;
                ">{mission.get('description', 'No mission description available.')}</p>
            </div>
        """, unsafe_allow_html=True)
    
    # Show mission difficulty
    if 'difficulty' in mission:
        difficulty_colors = {
            'Easy': '#28a745',
            'Medium': '#ffc107',
            'Hard': '#dc3545'
        }
        difficulty = mission['difficulty']
        color = difficulty_colors.get(difficulty, '#666')
        
        st.markdown(f"""
            <div style="margin: 10px 0;">
                <span style="
                    background-color: {color};
                    color: white;
                    padding: 5px 15px;
                    border-radius: 20px;
                    font-size: 14px;
                    font-weight: bold;
                ">Difficulty: {difficulty}</span>
            </div>
        """, unsafe_allow_html=True)


def render_submit_form():
    """
    Render form for submitting root cause conclusion.
    
    Returns:
        tuple: (user_conclusion, submit_clicked)
    """
    st.markdown("Analyze the data above and submit your conclusion about the root cause.")
    
    # Text input for conclusion
    user_conclusion = st.text_area(
        "Your Root Cause Analysis",
        placeholder="Enter your conclusion about what's causing the supply chain issues...",
        height=100,
        key="conclusion_input"
    )
    
    # Submit button
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        submit_clicked = submit_button("🔍 Submit Analysis")
    
    return user_conclusion, submit_clicked


def render_investigation_mode(data, mission):
    """
    Render complete investigation interface (legacy wrapper).
    
    Args:
        data (pd.DataFrame): The dataset to investigate
        mission (dict): Mission details
        
    Returns:
        tuple: (filtered_df, user_conclusion, submit_clicked)
    """
    return render_investigation(data, mission)

