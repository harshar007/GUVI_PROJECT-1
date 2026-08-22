import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st

def apply_custom_css():
    st.markdown("""
        <style>
            .main {
                background-color: #0E1117;
                color: #FAFAFA;
            }
            .metric-card {
                background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
                border: 1px solid #334155;
                border-radius: 12px;
                padding: 20px;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
                text-align: center;
                margin-bottom: 15px;
            }
            .metric-title {
                color: #94A3B8;
                font-size: 0.9rem;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.05em;
            }
            .metric-value {
                color: #38BDF8;
                font-size: 1.8rem;
                font-weight: 700;
                margin-top: 5px;
            }
            .stMetric {
                background-color: #1E293B;
                padding: 15px;
                border-radius: 10px;
            }
        </style>
    """, unsafe_allow_html=True)

def render_metric_card(title, value, prefix="", suffix=""):
    formatted_val = f"{prefix}{value}{suffix}"
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">{title}</div>
            <div class="metric-value">{formatted_val}</div>
        </div>
    """, unsafe_allow_html=True)

def plot_line_chart(df, x_col, y_col, title, x_label="Date", y_label="Value"):
    fig = px.line(df, x=x_col, y=y_col, title=title, markers=True, template="plotly_dark",
                  color_discrete_sequence=["#38BDF8"])
    fig.update_layout(xaxis_title=x_label, yaxis_title=y_label, margin=dict(l=20, r=20, t=40, b=20))
    return fig

def plot_bar_chart(df, x_col, y_col, title, orientation="v", color_col=None):
    if orientation == "h":
        fig = px.bar(df, y=x_col, x=y_col, title=title, orientation="h", template="plotly_dark",
                     color=color_col if color_col else y_col, color_continuous_scale="Viridis")
    else:
        fig = px.bar(df, x=x_col, y=y_col, title=title, template="plotly_dark",
                     color=color_col if color_col else y_col, color_continuous_scale="Viridis")
    fig.update_layout(margin=dict(l=20, r=20, t=40, b=20))
    return fig

def plot_pie_chart(df, names_col, values_col, title):
    fig = px.pie(df, names=names_col, values=values_col, title=title, template="plotly_dark",
                 hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(margin=dict(l=20, r=20, t=40, b=20))
    return fig
