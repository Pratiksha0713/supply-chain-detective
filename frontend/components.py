"""
Reusable UI Components Module

Common UI components and widgets used across different screens
in the Supply Chain Detective game.
"""

import streamlit as st


def kpi_card(label, value):
    """
    Render a styled KPI card with label and value.
    
    Args:
        label (str): The label/title for the KPI
        value (str/int/float): The value to display
    """
    st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            text-align: center;
            margin: 10px 0;
        ">
            <h4 style="
                color: white;
                margin: 0 0 10px 0;
                font-size: 14px;
                font-weight: 500;
                text-transform: uppercase;
                letter-spacing: 1px;
            ">{label}</h4>
            <p style="
                color: white;
                margin: 0;
                font-size: 32px;
                font-weight: bold;
            ">{value}</p>
        </div>
    """, unsafe_allow_html=True)


def alert_box(text):
    """
    Render a styled alert/warning box.
    
    Args:
        text (str): The alert message to display
    """
    st.markdown(f"""
        <div style="
            background-color: #fff3cd;
            border-left: 5px solid #ffc107;
            padding: 15px 20px;
            border-radius: 5px;
            margin: 15px 0;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        ">
            <div style="display: flex; align-items: center;">
                <span style="
                    font-size: 24px;
                    margin-right: 10px;
                    color: #856404;
                ">⚠️</span>
                <p style="
                    color: #856404;
                    margin: 0;
                    font-size: 16px;
                    line-height: 1.5;
                ">{text}</p>
            </div>
        </div>
    """, unsafe_allow_html=True)


def mission_header(text):
    """
    Render a styled mission header.
    
    Args:
        text (str): The mission header text
    """
    st.markdown(f"""
        <div style="
            background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
            padding: 30px;
            border-radius: 10px;
            margin: 20px 0;
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
        ">
            <h1 style="
                color: white;
                margin: 0;
                font-size: 36px;
                font-weight: bold;
                text-align: center;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
            ">🔍 {text}</h1>
        </div>
    """, unsafe_allow_html=True)


def submit_button(text):
    """
    Render a styled submit button.
    
    Args:
        text (str): The button text
        
    Returns:
        bool: True if button is clicked, False otherwise
    """
    # Create custom CSS for the button
    st.markdown("""
        <style>
        div.stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 40px;
            font-size: 18px;
            font-weight: bold;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
            width: 100%;
        }
        div.stButton > button:hover {
            background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
            transform: translateY(-2px);
        }
        div.stButton > button:active {
            transform: translateY(0);
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        </style>
    """, unsafe_allow_html=True)
    
    return st.button(text)


# Additional helper components

def render_header():
    """Render game header with title and navigation."""
    st.markdown("""
        <div style="
            background: linear-gradient(90deg, #141E30 0%, #243B55 100%);
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        ">
            <h1 style="
                color: white;
                margin: 0;
                text-align: center;
                font-size: 42px;
                font-weight: bold;
            ">🕵️ Supply Chain Detective 🔍</h1>
            <p style="
                color: #cccccc;
                text-align: center;
                margin: 10px 0 0 0;
                font-size: 16px;
            ">Investigate. Analyze. Solve.</p>
        </div>
    """, unsafe_allow_html=True)


def render_sidebar():
    """Render sidebar with game controls and info."""
    with st.sidebar:
        st.markdown("""
            <div style="
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 15px;
                border-radius: 10px;
                margin-bottom: 20px;
            ">
                <h2 style="color: white; margin: 0;">🎮 Game Menu</h2>
            </div>
        """, unsafe_allow_html=True)


def render_metric_card(title, value, delta=None):
    """
    Render styled metric card.
    
    Args:
        title (str): Metric title
        value (str/int/float): Metric value
        delta (str/int/float, optional): Change indicator
    """
    if delta is not None:
        st.metric(label=title, value=value, delta=delta)
    else:
        st.metric(label=title, value=value)


def render_chart_container(title, chart):
    """
    Render container for charts with title.
    
    Args:
        title (str): Chart title
        chart: Plotly or Matplotlib chart object
    """
    st.markdown(f"""
        <div style="
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            margin: 15px 0;
        ">
            <h3 style="margin-top: 0; color: #333;">{title}</h3>
        </div>
    """, unsafe_allow_html=True)
    st.plotly_chart(chart, use_container_width=True)


def render_info_box(message, type="info"):
    """
    Render styled information box.
    
    Args:
        message (str): The message to display
        type (str): Box type - "info", "success", "warning", "error"
    """
    colors = {
        "info": {"bg": "#d1ecf1", "border": "#0dcaf0", "text": "#055160", "icon": "ℹ️"},
        "success": {"bg": "#d1e7dd", "border": "#198754", "text": "#0f5132", "icon": "✅"},
        "warning": {"bg": "#fff3cd", "border": "#ffc107", "text": "#856404", "icon": "⚠️"},
        "error": {"bg": "#f8d7da", "border": "#dc3545", "text": "#842029", "icon": "❌"}
    }
    
    color_scheme = colors.get(type, colors["info"])
    
    st.markdown(f"""
        <div style="
            background-color: {color_scheme['bg']};
            border-left: 5px solid {color_scheme['border']};
            padding: 15px 20px;
            border-radius: 5px;
            margin: 15px 0;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        ">
            <div style="display: flex; align-items: center;">
                <span style="font-size: 24px; margin-right: 10px;">{color_scheme['icon']}</span>
                <p style="
                    color: {color_scheme['text']};
                    margin: 0;
                    font-size: 16px;
                    line-height: 1.5;
                ">{message}</p>
            </div>
        </div>
    """, unsafe_allow_html=True)


def render_loading_spinner():
    """Render loading spinner animation."""
    st.markdown("""
        <div style="text-align: center; padding: 20px;">
            <div style="
                border: 5px solid #f3f3f3;
                border-top: 5px solid #667eea;
                border-radius: 50%;
                width: 50px;
                height: 50px;
                animation: spin 1s linear infinite;
                margin: 0 auto;
            "></div>
            <p style="margin-top: 10px; color: #666;">Loading...</p>
        </div>
        <style>
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        </style>
    """, unsafe_allow_html=True)


def apply_custom_styling():
    """Apply custom CSS styling to app."""
    st.markdown("""
        <style>
        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 10px;
        }
        ::-webkit-scrollbar-track {
            background: #f1f1f1;
        }
        ::-webkit-scrollbar-thumb {
            background: #667eea;
            border-radius: 5px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #764ba2;
        }
        
        /* Custom font */
        body {
            font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        /* Improve overall spacing */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        </style>
    """, unsafe_allow_html=True)

