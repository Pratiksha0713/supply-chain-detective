"""
Dashboard UI Module

Main dashboard interface displaying KPIs, charts, and anomaly panels
for supply chain data visualization.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import sys
sys.path.append('frontend')

from components import kpi_card, alert_box, mission_header


def render_dashboard(sh_df, wh_df, delay_df, anomaly_df):
    """
    Render complete dashboard interface with KPIs, charts, and anomaly alerts.
    
    Args:
        sh_df (pd.DataFrame): Shipment data
        wh_df (pd.DataFrame): Warehouse data
        delay_df (pd.DataFrame): Delay data with time series
        anomaly_df (pd.DataFrame): Detected anomalies data
    """
    # Dashboard header
    mission_header("Supply Chain Analytics Dashboard")
    
    st.markdown("### 📊 Overview")
    st.write("Monitor key performance indicators and identify potential issues.")
    
    # Render KPI Cards
    render_kpi_cards(sh_df, delay_df)
    
    st.markdown("---")
    
    # Create two columns for charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Delay over time line chart
        render_delay_trend_chart(delay_df)
    
    with col2:
        # Supplier reliability bar chart
        render_supplier_comparison(sh_df)
    
    st.markdown("---")
    
    # Cost vs delay scatter plot
    render_cost_delay_scatter(sh_df, delay_df)
    
    st.markdown("---")
    
    # Anomaly alert panel
    render_anomaly_panel(anomaly_df)


def render_kpi_cards(sh_df, delay_df):
    """
    Render KPI metric cards at top of dashboard.
    
    Args:
        sh_df (pd.DataFrame): Shipment data
        delay_df (pd.DataFrame): Delay data
    """
    # Calculate KPIs
    total_shipments = len(sh_df) if sh_df is not None and not sh_df.empty else 0
    
    if delay_df is not None and not delay_df.empty and 'delay_days' in delay_df.columns:
        avg_delay = delay_df['delay_days'].mean()
        delayed_shipments = len(delay_df[delay_df['delay_days'] > 0])
        on_time_rate = ((total_shipments - delayed_shipments) / total_shipments * 100) if total_shipments > 0 else 0
    else:
        avg_delay = 0
        on_time_rate = 100
    
    if sh_df is not None and not sh_df.empty and 'cost' in sh_df.columns:
        total_cost = sh_df['cost'].sum()
    else:
        total_cost = 0
    
    # Display KPI cards in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        kpi_card("Total Shipments", f"{total_shipments:,}")
    
    with col2:
        kpi_card("Avg Delay", f"{avg_delay:.1f} days")
    
    with col3:
        kpi_card("On-Time Rate", f"{on_time_rate:.1f}%")
    
    with col4:
        kpi_card("Total Cost", f"${total_cost/1000:.1f}K")


def render_delay_trend_chart(delay_df):
    """
    Render line chart showing delay trends over time.
    
    Args:
        delay_df (pd.DataFrame): Delay data with time series
    """
    st.markdown("#### 📈 Delay Trend Over Time")
    
    if delay_df is None or delay_df.empty:
        st.info("No delay data available.")
        return
    
    # Check if we have date/time column
    date_col = None
    for col in ['date', 'ship_date', 'delivery_date', 'timestamp']:
        if col in delay_df.columns:
            date_col = col
            break
    
    if date_col is None:
        # Create a simple index-based chart
        fig = go.Figure()
        if 'delay_days' in delay_df.columns:
            fig.add_trace(go.Scatter(
                x=list(range(len(delay_df))),
                y=delay_df['delay_days'],
                mode='lines+markers',
                name='Delay',
                line=dict(color='#667eea', width=3),
                marker=dict(size=6)
            ))
        
        fig.update_layout(
            xaxis_title="Shipment Index",
            yaxis_title="Delay (days)",
            hovermode='x unified',
            height=350,
            margin=dict(l=0, r=0, t=30, b=0)
        )
    else:
        # Create time-based chart
        delay_df_sorted = delay_df.sort_values(date_col)
        
        fig = go.Figure()
        if 'delay_days' in delay_df.columns:
            fig.add_trace(go.Scatter(
                x=delay_df_sorted[date_col],
                y=delay_df_sorted['delay_days'],
                mode='lines+markers',
                name='Delay',
                line=dict(color='#667eea', width=3),
                marker=dict(size=6)
            ))
        
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Delay (days)",
            hovermode='x unified',
            height=350,
            margin=dict(l=0, r=0, t=30, b=0)
        )
    
    st.plotly_chart(fig, use_container_width=True)


def render_supplier_comparison(sh_df):
    """
    Render bar chart comparing supplier performance/reliability.
    
    Args:
        sh_df (pd.DataFrame): Shipment data
    """
    st.markdown("#### 📊 Supplier Reliability")
    
    if sh_df is None or sh_df.empty:
        st.info("No supplier data available.")
        return
    
    # Check for supplier column
    supplier_col = None
    for col in ['supplier', 'supplier_id', 'vendor', 'vendor_id']:
        if col in sh_df.columns:
            supplier_col = col
            break
    
    if supplier_col is None:
        st.warning("No supplier information found in data.")
        return
    
    # Calculate supplier metrics (on-time rate or avg delay)
    if 'delay_days' in sh_df.columns:
        supplier_metrics = sh_df.groupby(supplier_col).agg({
            'delay_days': 'mean'
        }).reset_index()
        supplier_metrics.columns = [supplier_col, 'avg_delay']
        supplier_metrics['reliability'] = 100 - (supplier_metrics['avg_delay'] * 10).clip(0, 100)
        
        # Sort by reliability
        supplier_metrics = supplier_metrics.sort_values('reliability', ascending=True)
        
        fig = go.Figure(go.Bar(
            x=supplier_metrics['reliability'],
            y=supplier_metrics[supplier_col],
            orientation='h',
            marker=dict(
                color=supplier_metrics['reliability'],
                colorscale='RdYlGn',
                showscale=True,
                colorbar=dict(title="Score")
            ),
            text=supplier_metrics['reliability'].round(1),
            textposition='outside'
        ))
        
        fig.update_layout(
            xaxis_title="Reliability Score (%)",
            yaxis_title="Supplier",
            height=350,
            margin=dict(l=0, r=0, t=30, b=0)
        )
    else:
        # Just count shipments by supplier
        supplier_counts = sh_df[supplier_col].value_counts().head(10)
        
        fig = go.Figure(go.Bar(
            x=supplier_counts.values,
            y=supplier_counts.index,
            orientation='h',
            marker=dict(color='#667eea')
        ))
        
        fig.update_layout(
            xaxis_title="Number of Shipments",
            yaxis_title="Supplier",
            height=350,
            margin=dict(l=0, r=0, t=30, b=0)
        )
    
    st.plotly_chart(fig, use_container_width=True)


def render_cost_delay_scatter(sh_df, delay_df):
    """
    Render scatter plot showing relationship between cost and delay.
    
    Args:
        sh_df (pd.DataFrame): Shipment data with cost
        delay_df (pd.DataFrame): Delay data
    """
    st.markdown("#### 💰 Cost vs Delay Analysis")
    
    if sh_df is None or sh_df.empty or delay_df is None or delay_df.empty:
        st.info("Insufficient data for cost vs delay analysis.")
        return
    
    # Merge dataframes if they have a common key
    if 'shipment_id' in sh_df.columns and 'shipment_id' in delay_df.columns:
        merged_df = pd.merge(sh_df, delay_df[['shipment_id', 'delay_days']], on='shipment_id', how='inner')
    elif 'cost' in delay_df.columns and 'delay_days' in delay_df.columns:
        merged_df = delay_df
    elif 'cost' in sh_df.columns and 'delay_days' in sh_df.columns:
        merged_df = sh_df
    else:
        st.warning("Unable to correlate cost and delay data.")
        return
    
    if 'cost' not in merged_df.columns or 'delay_days' not in merged_df.columns:
        st.warning("Cost or delay_days column not found.")
        return
    
    # Create scatter plot
    fig = px.scatter(
        merged_df,
        x='cost',
        y='delay_days',
        color='delay_days',
        size='cost' if len(merged_df) > 0 else None,
        color_continuous_scale='Reds',
        labels={'cost': 'Cost ($)', 'delay_days': 'Delay (days)'},
        hover_data={'cost': ':$,.2f', 'delay_days': ':.1f'}
    )
    
    fig.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')))
    
    fig.update_layout(
        height=400,
        margin=dict(l=0, r=0, t=30, b=0),
        coloraxis_colorbar=dict(title="Delay (days)")
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Add correlation insight
    if len(merged_df) > 1:
        correlation = merged_df['cost'].corr(merged_df['delay_days'])
        if abs(correlation) > 0.5:
            st.info(f"📊 Strong correlation detected: {correlation:.2f}. Higher costs {'correlate with' if correlation > 0 else 'inversely correlate with'} longer delays.")


def render_warehouse_metrics(wh_df):
    """
    Render warehouse performance metrics.
    
    Args:
        wh_df (pd.DataFrame): Warehouse data
    """
    st.markdown("#### 🏭 Warehouse Performance")
    
    if wh_df is None or wh_df.empty:
        st.info("No warehouse data available.")
        return
    
    # Calculate warehouse metrics
    if 'warehouse_id' in wh_df.columns:
        warehouse_summary = wh_df.groupby('warehouse_id').size().reset_index(name='shipments')
        
        fig = px.bar(
            warehouse_summary,
            x='warehouse_id',
            y='shipments',
            labels={'warehouse_id': 'Warehouse', 'shipments': 'Number of Shipments'},
            color='shipments',
            color_continuous_scale='Blues'
        )
        
        fig.update_layout(
            height=300,
            margin=dict(l=0, r=0, t=30, b=0)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No warehouse ID column found in data.")


def render_anomaly_panel(anomaly_df):
    """
    Render panel showing detected anomalies with alerts.
    
    Args:
        anomaly_df (pd.DataFrame): Detected anomalies data with anomaly indicators
    """
    st.markdown("### 🚨 Anomaly Detection Panel")
    
    if anomaly_df is None or anomaly_df.empty:
        st.success("✅ No anomalies detected. All systems operating normally.")
        return
    
    # Check for anomaly column
    anomaly_col = None
    for col in ['anomaly', 'is_anomaly', 'anomaly_flag']:
        if col in anomaly_df.columns:
            anomaly_col = col
            break
    
    if anomaly_col is None:
        st.warning("No anomaly indicator column found in data.")
        return
    
    # Filter for anomalies
    anomalies = anomaly_df[anomaly_df[anomaly_col] == 1] if anomaly_col in anomaly_df.columns else pd.DataFrame()
    
    if anomalies.empty:
        st.success("✅ No anomalies detected. All systems operating normally.")
    else:
        # Display alert
        alert_box(f"⚠️ {len(anomalies)} anomalies detected in the supply chain!")
        
        # Show anomaly details
        st.markdown(f"**Total Anomalies:** {len(anomalies)}")
        
        # Display anomalies in an expandable section
        with st.expander("📋 View Anomaly Details", expanded=True):
            # Show top 10 anomalies
            display_df = anomalies.head(10)
            
            # Select relevant columns to display
            display_cols = []
            for col in ['shipment_id', 'supplier', 'warehouse_id', 'delay_days', 'cost', 'anomaly_score']:
                if col in display_df.columns:
                    display_cols.append(col)
            
            if display_cols:
                st.dataframe(display_df[display_cols], use_container_width=True)
            else:
                st.dataframe(display_df, use_container_width=True)
            
            if len(anomalies) > 10:
                st.info(f"Showing 10 of {len(anomalies)} anomalies. Full analysis available in investigation mode.")
        
        # Anomaly distribution chart
        if len(anomalies) > 0:
            st.markdown("#### 📊 Anomaly Distribution")
            
            # If we have a timestamp or date column, show anomalies over time
            date_col = None
            for col in ['date', 'ship_date', 'delivery_date', 'timestamp']:
                if col in anomalies.columns:
                    date_col = col
                    break
            
            if date_col:
                anomaly_by_date = anomalies.groupby(date_col).size().reset_index(name='count')
                fig = px.line(
                    anomaly_by_date,
                    x=date_col,
                    y='count',
                    labels={date_col: 'Date', 'count': 'Number of Anomalies'},
                    markers=True
                )
                fig.update_traces(line_color='#dc3545', marker=dict(size=8))
            else:
                # Show by category if available
                category_col = None
                for col in ['supplier', 'warehouse_id', 'category']:
                    if col in anomalies.columns:
                        category_col = col
                        break
                
                if category_col:
                    anomaly_by_category = anomalies[category_col].value_counts().head(10)
                    fig = px.bar(
                        x=anomaly_by_category.index,
                        y=anomaly_by_category.values,
                        labels={'x': category_col.title(), 'y': 'Number of Anomalies'},
                        color=anomaly_by_category.values,
                        color_continuous_scale='Reds'
                    )
                else:
                    # Simple count chart
                    fig = px.bar(
                        x=['Detected Anomalies'],
                        y=[len(anomalies)],
                        labels={'x': '', 'y': 'Count'},
                        color=[len(anomalies)],
                        color_continuous_scale='Reds'
                    )
            
            fig.update_layout(
                height=300,
                margin=dict(l=0, r=0, t=30, b=0),
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)

