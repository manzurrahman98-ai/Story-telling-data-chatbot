-- Insert sample customers
INSERT INTO customers (name, email) VALUES
('John Doe', 'john@example.com'),
('Jane Smith', 'jane@example.com'),
('Bob Johnson', 'bob@example.com'),
('Alice Brown', 'alice@example.com'),
('Charlie Wilson', 'charlie@example.com');

-- Insert sample products
INSERT INTO products (name, category, price) VALUES
('Laptop', 'Electronics', 999.99),
('Mouse', 'Electronics', 29.99),
('Keyboard', 'Electronics', 79.99),
('Monitor', 'Electronics', 299.99),
('Desk Chair', 'Furniture', 199.99),
('Desk Lamp', 'Furniture', 39.99),
('Notebook', 'Stationery', 4.99),
('Pen Set', 'Stationery', 12.99);

-- Insert sample orders
INSERT INTO orders (customer_id, order_date, total_amount) VALUES
(1, '2024-01-15 10:30:00', 1029.98),
(1, '2024-02-20 14:15:00', 79.99),
(2, '2024-01-10 09:00:00', 329.98),
(3, '2024-01-25 16:45:00', 199.99),
(4, '2024-02-01 11:20:00', 42.98),
(5, '2024-02-10 13:30:00', 12.99);

-- Insert sample order items
INSERT INTO order_items (order_id, product_id, quantity, price) VALUES
(1, 1, 1, 999.99),
(1, 2, 1, 29.99),
(2, 3, 1, 79.99),
(3, 4, 1, 299.99),
(3, 2, 1, 29.99),
(4, 5, 1, 199.99),
(5, 6, 1, 39.99),
(5, 7, 1, 4.99),
(6, 8, 1, 12.99);
