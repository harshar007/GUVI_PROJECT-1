import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st

def apply_custom_css():
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
            
            html, body, [class*="css"] {
                font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            }
            
            /* Main Container Background */
            .main {
                background: radial-gradient(circle at 50% 0%, #1E1B4B 0%, #0F172A 50%, #090D16 100%);
                color: #F8FAFC;
            }
            
            /* Glassmorphic Metric Cards */
            .metric-card {
                background: rgba(30, 41, 59, 0.55);
                backdrop-filter: blur(16px);
                -webkit-backdrop-filter: blur(16px);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 16px;
                padding: 22px 18px;
                box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
                transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
                position: relative;
                overflow: hidden;
            }
            
            .metric-card:hover {
                transform: translateY(-4px);
                border-color: rgba(99, 102, 241, 0.4);
                box-shadow: 0 15px 35px -10px rgba(99, 102, 241, 0.25);
            }
            
            .metric-card::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 3px;
                background: linear-gradient(90deg, #06B6D4, #6366F1, #EC4899);
            }
            
            .metric-header {
                display: flex;
                align-items: center;
                justify-content: space-between;
                margin-bottom: 8px;
            }
            
            .metric-icon {
                font-size: 1.4rem;
                background: rgba(255, 255, 255, 0.06);
                padding: 8px;
                border-radius: 10px;
            }
            
            .metric-title {
                color: #94A3B8;
                font-size: 0.82rem;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.08em;
            }
            
            .metric-value {
                background: linear-gradient(135deg, #FFFFFF 0%, #CBD5E1 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                font-size: 1.85rem;
                font-weight: 800;
                letter-spacing: -0.02em;
            }
            
            .metric-subtitle {
                color: #64748B;
                font-size: 0.78rem;
                font-weight: 500;
                margin-top: 4px;
            }
            
            /* Sidebar Styling */
            [data-testid="stSidebar"] {
                background: rgba(15, 23, 42, 0.85);
                backdrop-filter: blur(20px);
                border-right: 1px solid rgba(255, 255, 255, 0.08);
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
                background: rgba(99, 102, 241, 0.2);
                color: #818CF8;
                border: 1px solid rgba(99, 102, 241, 0.3);
            }
            
            .badge-success {
                background: rgba(16, 185, 129, 0.2);
                color: #34D399;
                border: 1px solid rgba(16, 185, 129, 0.3);
            }
            
            /* Section Banners */
            .section-banner {
                background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.7) 100%);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 16px;
                padding: 24px;
                margin-bottom: 24px;
            }
            
            /* Custom Scrollbar */
            ::-webkit-scrollbar {
                width: 8px;
                height: 8px;
            }
            ::-webkit-scrollbar-track {
                background: #0F172A;
            }
            ::-webkit-scrollbar-thumb {
                background: #334155;
                border-radius: 4px;
            }
            ::-webkit-scrollbar-thumb:hover {
                background: #475569;
            }
            
            /* Streamlit Dataframe custom styling */
            [data-testid="stDataFrame"] {
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 12px;
                overflow: hidden;
            }
        </style>
    """, unsafe_allow_html=True)

def render_metric_card(title, value, prefix="", suffix="", icon="📊", subtitle=""):
    formatted_val = f"{prefix}{value}{suffix}"
    sub_html = f'<div class="metric-subtitle">{subtitle}</div>' if subtitle else ''
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-header">
                <span class="metric-title">{title}</span>
                <span class="metric-icon">{icon}</span>
            </div>
            <div class="metric-value">{formatted_val}</div>
            {sub_html}
        </div>
    """, unsafe_allow_html=True)

def plot_line_chart(df, x_col, y_col, title, x_label="Date", y_label="Value"):
    fig = px.line(
        df, x=x_col, y=y_col, title=title, markers=True, template="plotly_dark",
        color_discrete_sequence=["#38BDF8"]
    )
    fig.update_traces(
        line=dict(width=3, color='#06B6D4'),
        marker=dict(size=7, color='#6366F1', line=dict(width=2, color='#FFFFFF'))
    )
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(15, 23, 42, 0.5)',
        font=dict(family="Plus Jakarta Sans, sans-serif", color="#94A3B8"),
        title=dict(font=dict(size=16, color="#F8FAFC", family="Plus Jakarta Sans")),
        xaxis=dict(title=x_label, showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
        yaxis=dict(title=y_label, showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
        margin=dict(l=20, r=20, t=50, b=30)
    )
    return fig

def plot_bar_chart(df, x_col, y_col, title, orientation="v", color_col=None):
    colors = px.colors.sequential.Tealgrn if orientation == "h" else px.colors.sequential.Viridis
    if orientation == "h":
        fig = px.bar(
            df, y=x_col, x=y_col, title=title, orientation="h", template="plotly_dark",
            color=color_col if color_col else y_col, color_continuous_scale="Cividis"
        )
    else:
        fig = px.bar(
            df, x=x_col, y=y_col, title=title, template="plotly_dark",
            color=color_col if color_col else y_col, color_continuous_scale="Viridis"
        )
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(15, 23, 42, 0.5)',
        font=dict(family="Plus Jakarta Sans, sans-serif", color="#94A3B8"),
        title=dict(font=dict(size=16, color="#F8FAFC", family="Plus Jakarta Sans")),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
        margin=dict(l=20, r=20, t=50, b=30),
        coloraxis_showscale=False
    )
    fig.update_traces(marker=dict(cornerradius=6))
    return fig

def plot_pie_chart(df, names_col, values_col, title):
    fig = px.pie(
        df, names=names_col, values=values_col, title=title, template="plotly_dark",
        hole=0.55, color_discrete_sequence=["#06B6D4", "#6366F1", "#EC4899", "#10B981", "#F59E0B"]
    )
    fig.update_traces(
        textposition='outside', textinfo='percent+label',
        marker=dict(line=dict(color='#0F172A', width=2))
    )
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Plus Jakarta Sans, sans-serif", color="#94A3B8"),
        title=dict(font=dict(size=16, color="#F8FAFC", family="Plus Jakarta Sans")),
        margin=dict(l=20, r=20, t=50, b=30),
        showlegend=False
    )
    return fig
