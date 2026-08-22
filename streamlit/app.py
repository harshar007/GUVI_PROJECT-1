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

# Header Section
st.title("🛒 Cart2Insights: Decoding E-Commerce Performance")
st.markdown("### Strategic Business Insights, Sales & Operational Analytics Dashboard")

# Database Connection Info & Status
engine, db_type = get_db_engine()
st.sidebar.success(f"Connected to Database Engine: **{db_type}**")
st.sidebar.markdown("---")

# Navigation Sidebar
st.sidebar.header("Navigation")
menu_option = st.sidebar.radio(
    "Select Dashboard Section:",
    [
        "1. Business Overview",
        "2. Sales Analysis",
        "3. Customer Analysis",
        "4. Seller & Product Analysis",
        "5. Delivery Analysis",
        "6. Customer Experience & Hypothesis Testing"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("💡 Built with Python, SQL, Pandas, Plotly & Streamlit for GUVI/HCL Capstone.")

# ---------------------------------------------------------
# SECTION 1: BUSINESS OVERVIEW
# ---------------------------------------------------------
if menu_option == "1. Business Overview":
    st.header("📊 Business Overview & Key Performance Indicators")
    st.markdown("High-level executive metrics monitoring business scale, revenue, and customer satisfaction.")
    
    try:
        overview_df = run_query(QUERY_BUSINESS_OVERVIEW)
        if not overview_df.empty:
            row = overview_df.iloc[0]
            col1, col2, col3, col4, col5, col6 = st.columns(6)
            
            with col1:
                render_metric_card("Total Revenue", f"{row['total_revenue']:,.2f}", prefix="$")
            with col2:
                render_metric_card("Total Orders", f"{row['total_orders']:,}")
            with col3:
                render_metric_card("Total Customers", f"{row['total_customers']:,}")
            with col4:
                render_metric_card("Total Sellers", f"{row['total_sellers']:,}")
            with col5:
                render_metric_card("Avg Order Value", f"{row['average_order_value']:.2f}", prefix="$")
            with col6:
                render_metric_card("Avg Review Score", f"{row['avg_review_score']:.2f}", suffix=" / 5")
        
        st.markdown("---")
        st.subheader("📈 Monthly Order & Revenue Growth Trend")
        monthly_df = run_query(QUERY_MONTHLY_REVENUE)
        if not monthly_df.empty:
            col_chart1, col_chart2 = st.columns(2)
            with col_chart1:
                st.plotly_chart(plot_line_chart(monthly_df, 'month_year', 'monthly_revenue', "Monthly Revenue Trend ($)", "Month", "Revenue ($)"), use_container_width=True)
            with col_chart2:
                st.plotly_chart(plot_bar_chart(monthly_df, 'month_year', 'orders_count', "Monthly Orders Count", color_col='orders_count'), use_container_width=True)
    except Exception as e:
        st.error(f"Error fetching Business Overview data: {e}")

# ---------------------------------------------------------
# SECTION 2: SALES ANALYSIS
# ---------------------------------------------------------
elif menu_option == "2. Sales Analysis":
    st.header("📈 Sales & Revenue Optimization Analysis")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Top Revenue-Generating Product Categories")
        cat_df = run_query(QUERY_REVENUE_BY_CATEGORY)
        if not cat_df.empty:
            st.plotly_chart(plot_bar_chart(cat_df, 'category', 'category_revenue', "Revenue by Category ($)", orientation="h"), use_container_width=True)
            
    with col_b:
        st.subheader("Sales Revenue Distribution by Customer Location (State)")
        loc_df = run_query(QUERY_SALES_BY_LOCATION)
        if not loc_df.empty:
            st.plotly_chart(plot_bar_chart(loc_df, 'customer_state', 'total_revenue', "Revenue by Customer State ($)"), use_container_width=True)

    st.subheader("🔥 Top 10 Best-Selling Products")
    top_prod_df = run_query(QUERY_TOP_PRODUCTS)
    if not top_prod_df.empty:
        st.dataframe(top_prod_df, use_container_width=True)

# ---------------------------------------------------------
# SECTION 3: CUSTOMER ANALYSIS
# ---------------------------------------------------------
elif menu_option == "3. Customer Analysis":
    st.header("👥 Customer Behavior & Segmentation")
    
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.subheader("Repeat vs One-Time Customer Proportion")
        repeat_df = run_query(QUERY_REPEAT_VS_NEW)
        if not repeat_df.empty:
            st.plotly_chart(plot_pie_chart(repeat_df, 'customer_type', 'customer_count', "Customer Repeat Ratio"), use_container_width=True)
            
    with col_c2:
        st.subheader("Customer Spending Segmentation")
        spend_df = run_query(QUERY_CUSTOMER_SPENDING)
        if not spend_df.empty:
            segment_counts = spend_df['customer_segment'].value_counts().reset_index()
            segment_counts.columns = ['customer_segment', 'count']
            st.plotly_chart(plot_pie_chart(segment_counts, 'customer_segment', 'count', "Customer Segments"), use_container_width=True)

    st.subheader("💎 Top High-Value VIP Customers")
    if not spend_df.empty:
        st.dataframe(spend_df.head(15), use_container_width=True)

# ---------------------------------------------------------
# SECTION 4: SELLER & PRODUCT ANALYSIS
# ---------------------------------------------------------
elif menu_option == "4. Seller & Product Analysis":
    st.header("🏬 Seller & Product Performance Analysis")
    
    st.subheader("🏆 Top Performing Sellers by Revenue & Order Fulfillment")
    seller_df = run_query(QUERY_SELLER_PERFORMANCE)
    if not seller_df.empty:
        st.plotly_chart(plot_bar_chart(seller_df, 'seller_id', 'total_revenue', "Seller Total Revenue ($)", color_col='orders_fulfilled'), use_container_width=True)
        st.dataframe(seller_df, use_container_width=True)

# ---------------------------------------------------------
# SECTION 5: DELIVERY ANALYSIS
# ---------------------------------------------------------
elif menu_option == "5. Delivery Analysis":
    st.header("🚚 Delivery & Operational Optimization")
    
    st.subheader("Average Delivery Time by State (Days)")
    delivery_df = run_query(QUERY_DELIVERY_PERFORMANCE)
    if not delivery_df.empty:
        st.plotly_chart(plot_bar_chart(delivery_df, 'customer_state', 'avg_delivery_days', "Average Delivery Days per State"), use_container_width=True)
        st.dataframe(delivery_df, use_container_width=True)

# ---------------------------------------------------------
# SECTION 6: CUSTOMER EXPERIENCE & HYPOTHESIS TESTING
# ---------------------------------------------------------
elif menu_option == "6. Customer Experience & Hypothesis Testing":
    st.header("⭐ Customer Experience & Statistical Hypothesis Testing")
    
    col_e1, col_e2 = st.columns(2)
    with col_e1:
        st.subheader("Customer Review Score Distribution")
        review_df = run_query(QUERY_REVIEW_SCORE_DISTRIBUTION)
        if not review_df.empty:
            st.plotly_chart(plot_bar_chart(review_df, 'review_score', 'total_reviews', "Reviews Count by Score"), use_container_width=True)
            
    with col_e2:
        st.subheader("Impact of Delivery Delay on Review Rating")
        delay_rating_df = run_query(QUERY_DELIVERY_DELAY_VS_RATING)
        if not delay_rating_df.empty:
            st.plotly_chart(plot_bar_chart(delay_rating_df, 'delivery_status', 'average_review_score', "Average Rating: Delayed vs On-Time"), use_container_width=True)

    st.markdown("---")
    st.subheader("🧪 Statistical Analysis & Hypothesis Testing Results")
    
    stats_json_path = os.path.join(os.path.dirname(__file__), "..", "data", "cleaned", "statistical_results.json")
    if os.path.exists(stats_json_path):
        with open(stats_json_path, "r") as f:
            stats_data = json.load(f)
            
        t1, t2, t3 = st.tabs(["1. T-Test (Delivery vs Rating)", "2. ANOVA (Category vs AOV)", "3. Chi-Square (Payment vs Status)"])
        
        with t1:
            tt = stats_data.get("t_test", {})
            st.markdown(f"#### {tt.get('title')}")
            st.write(f"**Method:** {tt.get('method')}")
            st.write(f"**T-Statistic:** `{tt.get('t_stat'):.4f}` | **P-Value:** `{tt.get('p_value'):.4e}`")
            st.write(f"**On-time Orders Mean Score:** `{tt.get('ontime_mean'):.2f}` | **Delayed Orders Mean Score:** `{tt.get('delayed_mean'):.2f}`")
            st.info(f"**Business Decision & Insight:** {tt.get('conclusion')}")

        with t2:
            an = stats_data.get("anova", {})
            st.markdown(f"#### {an.get('title')}")
            st.write(f"**Method:** {an.get('method')}")
            st.write(f"**F-Statistic:** `{an.get('f_stat'):.4f}` | **P-Value:** `{an.get('p_value'):.4e}`")
            st.info(f"**Business Decision & Insight:** {an.get('conclusion')}")

        with t3:
            cs = stats_data.get("chi_square", {})
            st.markdown(f"#### {cs.get('title')}")
            st.write(f"**Method:** {cs.get('method')}")
            st.write(f"**Chi2-Statistic:** `{cs.get('chi2_stat'):.4f}` | **P-Value:** `{cs.get('p_value'):.4e}`")
            st.info(f"**Business Decision & Insight:** {cs.get('conclusion')}")
