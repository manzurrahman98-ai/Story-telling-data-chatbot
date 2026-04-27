SCHEMA_DESCRIPTION = """
Database Schema for E-commerce System:

Table: customers
- id (INTEGER, PRIMARY KEY) - Unique customer identifier
- name (VARCHAR) - Customer's full name
- email (VARCHAR) - Customer's email address (unique)
- created_at (TIMESTAMP) - When customer registered

Table: orders
- id (INTEGER, PRIMARY KEY) - Unique order identifier
- customer_id (INTEGER, FOREIGN KEY references customers.id)
- order_date (TIMESTAMP) - When order was placed
- total_amount (DECIMAL) - Total order amount

Table: products
- id (INTEGER, PRIMARY KEY) - Unique product identifier
- name (VARCHAR) - Product name
- category (VARCHAR) - Product category
- price (DECIMAL) - Product price

Table: order_items
- id (INTEGER, PRIMARY KEY) - Unique item identifier
- order_id (INTEGER, FOREIGN KEY references orders.id)
- product_id (INTEGER, FOREIGN KEY references products.id)
- quantity (INTEGER) - Number of units ordered
- price (DECIMAL) - Price at time of order

Common Query Patterns:
- Sales analysis: SUM(quantity * price) or SUM(total_amount)
- Customer behavior: COUNT(orders) per customer, average order value
- Product performance: Top products by quantity or revenue
- Time-based analysis: GROUP BY date_trunc('month', order_date)
"""
