import streamlit as st
import pandas as pd
import json
import os
from database import run_query, get_db_engine
from queries import (
    QUERY_BUSINESS_OVERVIEW, QUERY_MONTHLY_REVENUE, QUERY_REVENUE_BY_CATEGORY,
    QUERY_TOP_PRODUCTS, QUERY_SALES_BY_LOCATION, QUERY_CUSTOMER_SPENDING,
    QUERY_REPEAT_VS_NEW, QUERY_SELLER_PERFORMANCE, QUERY_DELIVERY_PERFORMANCE,
    QUERY_DELIVERY_DELAY_VS_RATING, QUERY_REVIEW_SCORE_DISTRIBUTION
)
from utils import (
    apply_custom_css, render_metric_card, plot_line_chart, plot_bar_chart, plot_pie_chart
)

st.set_page_config(
    page_title="Cart2Insights | E-Commerce Analytics",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_custom_css()

# Header Hero Banner
st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%); 
                border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 20px; padding: 28px 32px; margin-bottom: 28px;
                box-shadow: 0 15px 35px -10px rgba(0, 0, 0, 0.5);">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
            <div>
                <span class="badge badge-primary">GUVI / HCL CAPSTONE SOLUTION</span>
                <h1 style="background: linear-gradient(135deg, #FFFFFF 0%, #38BDF8 100%); -webkit-background-clip: text; 
                           -webkit-text-fill-color: transparent; font-size: 2.4rem; font-weight: 800; margin: 10px 0 6px 0;">
                    🛒 Cart2Insights: E-Commerce Analytics Platform
                </h1>
                <p style="color: #94A3B8; font-size: 1.05rem; font-weight: 500; margin: 0;">
                    Decoding E-Commerce Sales Performance, Operational Logistics, Customer Retention & Statistical Insights
                </p>
            </div>
            <div style="margin-top: 10px;">
                <span class="badge badge-success">⚡ Live Database Active</span>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Database Engine Status
engine, db_type = get_db_engine()
st.sidebar.markdown(f"""
    <div style="background: rgba(30, 41, 59, 0.6); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 14px; margin-bottom: 20px;">
        <div style="color: #94A3B8; font-size: 0.75rem; font-weight: 700; text-transform: uppercase;">Connected Engine</div>
        <div style="color: #38BDF8; font-size: 1.1rem; font-weight: 800; margin-top: 2px;">⚡ {db_type} Database</div>
    </div>
""", unsafe_allow_html=True)

# Navigation Sidebar
st.sidebar.markdown("### 🧭 Operational Modules")
menu_option = st.sidebar.radio(
    "Select Dashboard View:",
    [
        "📊 Business Overview",
        "📈 Sales Analysis",
        "👥 Customer Analysis",
        "🏬 Seller & Product Performance",
        "🚚 Delivery & Operations",
        "🧪 Statistical Hypothesis Testing"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
    <div style="color: #64748B; font-size: 0.8rem; text-align: center;">
        Developed for <b>GUVI & HCL Tech Capstone</b><br/>
        Python • SQL • Pandas • Plotly • Streamlit
    </div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# SECTION 1: BUSINESS OVERVIEW
# ---------------------------------------------------------
if menu_option == "📊 Business Overview":
    st.markdown("### 📊 Executive KPIs & Performance Summary")
    
    try:
        overview_df = run_query(QUERY_BUSINESS_OVERVIEW)
        if not overview_df.empty:
            row = overview_df.iloc[0]
            col1, col2, col3, col4, col5, col6 = st.columns(6)
            
            with col1:
                render_metric_card("Total Revenue", f"{row['total_revenue']:,.2f}", prefix="$", icon="💰", subtitle="Net Sales Revenue")
            with col2:
                render_metric_card("Total Orders", f"{row['total_orders']:,}", icon="📦", subtitle="Fulfilled Orders")
            with col3:
                render_metric_card("Total Customers", f"{row['total_customers']:,}", icon="👥", subtitle="Unique Customers")
            with col4:
                render_metric_card("Total Sellers", f"{row['total_sellers']:,}", icon="🏬", subtitle="Active Merchants")
            with col5:
                render_metric_card("Avg Order Value", f"{row['average_order_value']:.2f}", prefix="$", icon="💳", subtitle="Revenue per Order")
            with col6:
                render_metric_card("Avg Rating", f"{row['avg_review_score']:.2f}", suffix=" / 5", icon="⭐", subtitle="Customer Score")
        
        st.markdown("<br/>", unsafe_allow_html=True)
        st.markdown("### 📈 Monthly Order Volume & Revenue Growth Trends")
        monthly_df = run_query(QUERY_MONTHLY_REVENUE)
        if not monthly_df.empty:
            col_chart1, col_chart2 = st.columns(2)
            with col_chart1:
                st.plotly_chart(
                    plot_line_chart(monthly_df, 'month_year', 'monthly_revenue', "Monthly Revenue Trend ($)", "Month", "Revenue ($)"),
                    use_container_width=True
                )
            with col_chart2:
                st.plotly_chart(
                    plot_bar_chart(monthly_df, 'month_year', 'orders_count', "Monthly Fulfilled Orders Count", color_col='orders_count'),
                    use_container_width=True
                )
    except Exception as e:
        st.error(f"Error loading Business Overview metrics: {e}")

# ---------------------------------------------------------
# SECTION 2: SALES ANALYSIS
# ---------------------------------------------------------
elif menu_option == "📈 Sales Analysis":
    st.markdown("### 📈 Sales & Product Category Revenue Breakdown")
    
    col_a, col_b = st.columns(2)
    with col_a:
        cat_df = run_query(QUERY_REVENUE_BY_CATEGORY)
        if not cat_df.empty:
            st.plotly_chart(
                plot_bar_chart(cat_df, 'category', 'category_revenue', "Top 10 Product Categories by Revenue ($)", orientation="h"),
                use_container_width=True
            )
            
    with col_b:
        loc_df = run_query(QUERY_SALES_BY_LOCATION)
        if not loc_df.empty:
            st.plotly_chart(
                plot_bar_chart(loc_df, 'customer_state', 'total_revenue', "State-Level Sales Revenue Distribution ($)"),
                use_container_width=True
            )

    st.markdown("### 🔥 Top Best-Selling Products Leaderboard")
    top_prod_df = run_query(QUERY_TOP_PRODUCTS)
    if not top_prod_df.empty:
        st.dataframe(top_prod_df, use_container_width=True, height=360)

# ---------------------------------------------------------
# SECTION 3: CUSTOMER ANALYSIS
# ---------------------------------------------------------
elif menu_option == "👥 Customer Analysis":
    st.markdown("### 👥 Customer Retention & Spending Segmentation")
    
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        repeat_df = run_query(QUERY_REPEAT_VS_NEW)
        if not repeat_df.empty:
            st.plotly_chart(
                plot_pie_chart(repeat_df, 'customer_type', 'customer_count', "Repeat vs One-Time Customer Ratio"),
                use_container_width=True
            )
            
    with col_c2:
        spend_df = run_query(QUERY_CUSTOMER_SPENDING)
        if not spend_df.empty:
            segment_counts = spend_df['customer_segment'].value_counts().reset_index()
            segment_counts.columns = ['customer_segment', 'count']
            st.plotly_chart(
                plot_pie_chart(segment_counts, 'customer_segment', 'count', "Customer Spending Tier Distribution"),
                use_container_width=True
            )

    st.markdown("### 💎 Top High-Value VIP Customers")
    if not spend_df.empty:
        st.dataframe(spend_df.head(15), use_container_width=True, height=380)

# ---------------------------------------------------------
# SECTION 4: SELLER & PRODUCT PERFORMANCE
# ---------------------------------------------------------
elif menu_option == "🏬 Seller & Product Performance":
    st.markdown("### 🏬 Merchant & Seller Performance Dashboard")
    
    seller_df = run_query(QUERY_SELLER_PERFORMANCE)
    if not seller_df.empty:
        st.plotly_chart(
            plot_bar_chart(seller_df, 'seller_id', 'total_revenue', "Top Sellers by Revenue ($)", color_col='orders_fulfilled'),
            use_container_width=True
        )
        st.markdown("### 🏆 Seller Scoreboard & Fulfillment Metrics")
        st.dataframe(seller_df, use_container_width=True, height=380)

# ---------------------------------------------------------
# SECTION 5: DELIVERY & OPERATIONS
# ---------------------------------------------------------
elif menu_option == "🚚 Delivery & Operations":
    st.markdown("### 🚚 Logistics & Delivery Speed Metrics")
    
    delivery_df = run_query(QUERY_DELIVERY_PERFORMANCE)
    if not delivery_df.empty:
        st.plotly_chart(
            plot_bar_chart(delivery_df, 'customer_state', 'avg_delivery_days', "Average Delivery Duration per State (Days)"),
            use_container_width=True
        )
        st.markdown("### 📍 State-Level Delivery Performance Details")
        st.dataframe(delivery_df, use_container_width=True, height=380)

# ---------------------------------------------------------
# SECTION 6: STATISTICAL HYPOTHESIS TESTING
# ---------------------------------------------------------
elif menu_option == "🧪 Statistical Hypothesis Testing":
    st.markdown("### 🧪 Statistical Analysis & Hypothesis Testing")
    
    col_e1, col_e2 = st.columns(2)
    with col_e1:
        review_df = run_query(QUERY_REVIEW_SCORE_DISTRIBUTION)
        if not review_df.empty:
            st.plotly_chart(
                plot_bar_chart(review_df, 'review_score', 'total_reviews', "Customer Review Rating Score Distribution"),
                use_container_width=True
            )
            
    with col_e2:
        delay_rating_df = run_query(QUERY_DELIVERY_DELAY_VS_RATING)
        if not delay_rating_df.empty:
            st.plotly_chart(
                plot_bar_chart(delay_rating_df, 'delivery_status', 'average_review_score', "Average Rating Score: Delayed vs On-Time"),
                use_container_width=True
            )

    st.markdown("<br/>", unsafe_allow_html=True)
    st.markdown("### 📋 Statistical Test Results & Rigorous Verification")
    
    stats_json_path = os.path.join(os.path.dirname(__file__), "..", "data", "cleaned", "statistical_results.json")
    if os.path.exists(stats_json_path):
        with open(stats_json_path, "r", encoding="utf-8") as f:
            stats_data = json.load(f)
            
        t1, t2, t3 = st.tabs(["1️⃣ Welch's T-Test (Delivery vs Rating)", "2️⃣ One-Way ANOVA (Category vs AOV)", "3️⃣ Chi-Square Test (Payment vs Status)"])
        
        with t1:
            tt = stats_data.get("t_test", {})
            st.markdown(f"#### 📊 {tt.get('title')}")
            st.markdown(f"**Statistical Method:** `{tt.get('method')}`")
            st.markdown(f"**T-Statistic:** `{tt.get('t_stat'):.4f}` | **P-Value:** `{tt.get('p_value'):.4e}`")
            st.markdown(f"**On-Time Orders Mean Rating:** `{tt.get('ontime_mean'):.2f} / 5.0` | **Delayed Orders Mean Rating:** `{tt.get('delayed_mean'):.2f} / 5.0`")
            st.info(f"💡 **Business Decision & Insight:** {tt.get('conclusion')}")

        with t2:
            an = stats_data.get("anova", {})
            st.markdown(f"#### 📊 {an.get('title')}")
            st.markdown(f"**Statistical Method:** `{an.get('method')}`")
            st.markdown(f"**F-Statistic:** `{an.get('f_stat'):.4f}` | **P-Value:** `{an.get('p_value'):.4e}`")
            st.info(f"💡 **Business Decision & Insight:** {an.get('conclusion')}")

        with t3:
            cs = stats_data.get("chi_square", {})
            st.markdown(f"#### 📊 {cs.get('title')}")
            st.markdown(f"**Statistical Method:** `{cs.get('method')}`")
            st.markdown(f"**Chi-Square Statistic ($\chi^2$):** `{cs.get('chi2_stat'):.4f}` | **Degrees of Freedom (dof):** `{cs.get('dof')}` | **P-Value:** `{cs.get('p_value'):.4e}`")
            st.info(f"💡 **Business Decision & Insight:** {cs.get('conclusion')}")
