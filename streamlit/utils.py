import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st

def apply_custom_css():
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
            
            html, body, [class*="css"], [data-testid="stAppViewContainer"], .stApp {
                background-color: #FFFFFF !important;
                color: #000000 !important;
                font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            }
            
            /* Sidebar Styling */
            [data-testid="stSidebar"] {
                background-color: #F9FAFB !important;
                border-right: 1px solid #E5E7EB !important;
            }
            
            [data-testid="stSidebar"] * {
                color: #111827 !important;
            }
            
            /* Metric Cards */
            .metric-card {
                background: #FFFFFF;
                border: 1px solid #E5E7EB;
                border-radius: 12px;
                padding: 20px 16px;
                box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
                position: relative;
                overflow: hidden;
            }
            
            .metric-card::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 3px;
                background: #2563EB;
            }
            
            .metric-header {
                display: flex;
                align-items: center;
                justify-content: space-between;
                margin-bottom: 6px;
            }
            
            .metric-title {
                color: #4B5563;
                font-size: 0.8rem;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.05em;
            }
            
            .metric-value {
                color: #000000;
                font-size: 1.8rem;
                font-weight: 800;
                letter-spacing: -0.02em;
            }
            
            .metric-subtitle {
                color: #6B7280;
                font-size: 0.78rem;
                font-weight: 500;
                margin-top: 4px;
            }
            
            /* Badges & Pills */
            .badge {
                display: inline-block;
                padding: 4px 12px;
                border-radius: 9999px;
                font-size: 0.75rem;
                font-weight: 700;
                letter-spacing: 0.05em;
                text-transform: uppercase;
            }
            
            .badge-primary {
                background: #EFF6FF;
                color: #1D4ED8;
                border: 1px solid #BFDBFE;
            }
            
            .badge-success {
                background: #ECFDF5;
                color: #047857;
                border: 1px solid #A7F3D0;
            }
            
            /* Custom Scrollbar */
            ::-webkit-scrollbar {
                width: 8px;
                height: 8px;
            }
            ::-webkit-scrollbar-track {
                background: #F3F4F6;
            }
            ::-webkit-scrollbar-thumb {
                background: #D1D5DB;
                border-radius: 4px;
            }
            ::-webkit-scrollbar-thumb:hover {
                background: #9CA3AF;
            }
            
            /* Streamlit Dataframe custom styling */
            [data-testid="stDataFrame"] {
                border: 1px solid #E5E7EB;
                border-radius: 8px;
                overflow: hidden;
            }
        </style>
    """, unsafe_allow_html=True)

def render_metric_card(title, value, prefix="", suffix="", icon="", subtitle=""):
    formatted_val = f"{prefix}{value}{suffix}"
    sub_html = f'<div class="metric-subtitle">{subtitle}</div>' if subtitle else ''
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-header">
                <span class="metric-title">{title}</span>
            </div>
            <div class="metric-value">{formatted_val}</div>
            {sub_html}
        </div>
    """, unsafe_allow_html=True)

def plot_line_chart(df, x_col, y_col, title, x_label="Date", y_label="Value"):
    fig = px.line(
        df, x=x_col, y=y_col, title=title, markers=True, template="plotly_white",
        color_discrete_sequence=["#2563EB"]
    )
    fig.update_traces(
        line=dict(width=3, color='#2563EB'),
        marker=dict(size=7, color='#1D4ED8', line=dict(width=2, color='#FFFFFF'))
    )
    fig.update_layout(
        paper_bgcolor='#FFFFFF',
        plot_bgcolor='#FFFFFF',
        font=dict(family="Plus Jakarta Sans, sans-serif", color="#111827"),
        title=dict(font=dict(size=16, color="#000000", family="Plus Jakarta Sans")),
        xaxis=dict(title=x_label, showgrid=True, gridcolor='#E5E7EB'),
        yaxis=dict(title=y_label, showgrid=True, gridcolor='#E5E7EB'),
        margin=dict(l=20, r=20, t=50, b=30)
    )
    return fig

def plot_bar_chart(df, x_col, y_col, title, orientation="v", color_col=None):
    if orientation == "h":
        fig = px.bar(
            df, y=x_col, x=y_col, title=title, orientation="h", template="plotly_white",
            color=color_col if color_col else y_col, color_continuous_scale="Blues"
        )
    else:
        fig = px.bar(
            df, x=x_col, y=y_col, title=title, template="plotly_white",
            color=color_col if color_col else y_col, color_continuous_scale="Blues"
        )
    fig.update_layout(
        paper_bgcolor='#FFFFFF',
        plot_bgcolor='#FFFFFF',
        font=dict(family="Plus Jakarta Sans, sans-serif", color="#111827"),
        title=dict(font=dict(size=16, color="#000000", family="Plus Jakarta Sans")),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#E5E7EB'),
        margin=dict(l=20, r=20, t=50, b=30),
        coloraxis_showscale=False
    )
    fig.update_traces(marker=dict(cornerradius=4))
    return fig

def plot_pie_chart(df, names_col, values_col, title):
    fig = px.pie(
        df, names=names_col, values=values_col, title=title, template="plotly_white",
        hole=0.55, color_discrete_sequence=["#2563EB", "#0D9488", "#D97706", "#DC2626", "#4F46E5"]
    )
    fig.update_traces(
        textposition='outside', textinfo='percent+label',
        marker=dict(line=dict(color='#FFFFFF', width=2))
    )
    fig.update_layout(
        paper_bgcolor='#FFFFFF',
        plot_bgcolor='#FFFFFF',
        font=dict(family="Plus Jakarta Sans, sans-serif", color="#111827"),
        title=dict(font=dict(size=16, color="#000000", family="Plus Jakarta Sans")),
        margin=dict(l=20, r=20, t=50, b=30),
        showlegend=False
    )
    return fig
