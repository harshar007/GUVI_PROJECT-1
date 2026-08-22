# SQL Queries for Streamlit Dashboard & Business Analysis

# 1. Business Overview Queries
QUERY_BUSINESS_OVERVIEW = """
SELECT 
    (SELECT COUNT(DISTINCT order_id) FROM orders) AS total_orders,
    (SELECT COUNT(DISTINCT customer_id) FROM customers) AS total_customers,
    (SELECT COUNT(DISTINCT seller_id) FROM sellers) AS total_sellers,
    (SELECT SUM(price + freight_value) FROM order_items) AS total_revenue,
    (SELECT AVG(price + freight_value) FROM order_items) AS average_order_value,
    (SELECT AVG(review_score) FROM order_reviews) AS avg_review_score;
"""

# 2. Sales Analysis Queries
QUERY_MONTHLY_REVENUE = """
SELECT 
    STRFTIME('%Y-%m', o.order_purchase_timestamp) AS month_year,
    COUNT(DISTINCT o.order_id) AS orders_count,
    ROUND(SUM(oi.price + oi.freight_value), 2) AS monthly_revenue
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.order_purchase_timestamp IS NOT NULL
GROUP BY month_year
ORDER BY month_year ASC;
"""

QUERY_REVENUE_BY_CATEGORY = """
SELECT 
    COALESCE(t.product_category_name_english, p.product_category_name) AS category,
    COUNT(DISTINCT oi.order_id) AS total_orders,
    ROUND(SUM(oi.price + oi.freight_value), 2) AS category_revenue,
    ROUND(AVG(oi.price), 2) AS avg_price
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
LEFT JOIN product_category_name_translation t ON p.product_category_name = t.product_category_name
GROUP BY category
ORDER BY category_revenue DESC
LIMIT 15;
"""

QUERY_TOP_PRODUCTS = """
SELECT 
    p.product_id,
    COALESCE(t.product_category_name_english, p.product_category_name) AS category,
    COUNT(oi.order_item_id) AS units_sold,
    ROUND(SUM(oi.price), 2) AS total_sales
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
LEFT JOIN product_category_name_translation t ON p.product_category_name = t.product_category_name
GROUP BY p.product_id, category
ORDER BY units_sold DESC
LIMIT 10;
"""

QUERY_SALES_BY_LOCATION = """
SELECT 
    c.customer_state,
    COUNT(DISTINCT o.order_id) AS total_orders,
    COUNT(DISTINCT c.customer_unique_id) AS total_customers,
    ROUND(SUM(oi.price + oi.freight_value), 2) AS total_revenue
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY c.customer_state
ORDER BY total_revenue DESC;
"""

# 3. Customer Analysis Queries
QUERY_CUSTOMER_SPENDING = """
WITH CustomerSpend AS (
    SELECT 
        c.customer_unique_id,
        COUNT(DISTINCT o.order_id) AS order_count,
        ROUND(SUM(oi.price + oi.freight_value), 2) AS total_spent
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    JOIN order_items oi ON o.order_id = oi.order_id
    GROUP BY c.customer_unique_id
)
SELECT 
    customer_unique_id,
    order_count,
    total_spent,
    CASE 
        WHEN total_spent > 1000 THEN 'VIP High Spender'
        WHEN total_spent BETWEEN 300 AND 1000 THEN 'Medium Spender'
        ELSE 'Regular Spender'
    END AS customer_segment
FROM CustomerSpend
ORDER BY total_spent DESC;
"""

QUERY_REPEAT_VS_NEW = """
WITH OrderCounts AS (
    SELECT 
        c.customer_unique_id,
        COUNT(DISTINCT o.order_id) AS num_orders
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_unique_id
)
SELECT 
    CASE WHEN num_orders > 1 THEN 'Repeat Customer' ELSE 'One-Time Customer' END AS customer_type,
    COUNT(customer_unique_id) AS customer_count
FROM OrderCounts
GROUP BY customer_type;
"""

# 4. Seller & Product Analysis Queries
QUERY_SELLER_PERFORMANCE = """
SELECT 
    s.seller_id,
    s.seller_state,
    COUNT(DISTINCT oi.order_id) AS orders_fulfilled,
    ROUND(SUM(oi.price + oi.freight_value), 2) AS total_revenue,
    ROUND(AVG(r.review_score), 2) AS avg_seller_rating
FROM sellers s
JOIN order_items oi ON s.seller_id = oi.seller_id
LEFT JOIN order_reviews r ON oi.order_id = r.order_id
GROUP BY s.seller_id, s.seller_state
ORDER BY total_revenue DESC
LIMIT 15;
"""

# 5. Delivery Analysis Queries
QUERY_DELIVERY_PERFORMANCE = """
SELECT 
    c.customer_state,
    ROUND(AVG(JULIANDAY(o.order_delivered_customer_date) - JULIANDAY(o.order_purchase_timestamp)), 2) AS avg_delivery_days,
    SUM(CASE WHEN JULIANDAY(o.order_delivered_customer_date) > JULIANDAY(o.order_estimated_delivery_date) THEN 1 ELSE 0 END) AS delayed_orders,
    SUM(CASE WHEN JULIANDAY(o.order_delivered_customer_date) <= JULIANDAY(o.order_estimated_delivery_date) THEN 1 ELSE 0 END) AS ontime_orders,
    COUNT(o.order_id) AS total_delivered_orders
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.order_status = 'delivered' 
  AND o.order_delivered_customer_date IS NOT NULL
GROUP BY c.customer_state
ORDER BY avg_delivery_days ASC;
"""

QUERY_DELIVERY_DELAY_VS_RATING = """
SELECT 
    CASE 
        WHEN JULIANDAY(o.order_delivered_customer_date) > JULIANDAY(o.order_estimated_delivery_date) THEN 'Delayed'
        ELSE 'On-Time'
    END AS delivery_status,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(AVG(r.review_score), 2) AS average_review_score
FROM orders o
JOIN order_reviews r ON o.order_id = r.order_id
WHERE o.order_status = 'delivered' AND o.order_delivered_customer_date IS NOT NULL
GROUP BY delivery_status;
"""

# 6. Customer Experience Queries
QUERY_REVIEW_SCORE_DISTRIBUTION = """
SELECT 
    review_score,
    COUNT(review_id) AS total_reviews,
    ROUND(COUNT(review_id) * 100.0 / (SELECT COUNT(*) FROM order_reviews), 2) AS percentage
FROM order_reviews
GROUP BY review_score
ORDER BY review_score DESC;
"""
