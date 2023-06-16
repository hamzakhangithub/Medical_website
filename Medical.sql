CREATE TABLE Medical_Items (
    item_id INT PRIMARY KEY,
    item_name VARCHAR(50),
    category VARCHAR(20),
    price DECIMAL(8,2),
    stock_quantity INT
);

CREATE TABLE Medical_Sales (
    sale_id INT PRIMARY KEY,
    sale_date DATE,
    item_id INT,
    quantity INT,
    total_amount DECIMAL(8,2),
    FOREIGN KEY (item_id) REFERENCES Medical_Items(item_id)
);

INSERT INTO Medical_Items (item_id, item_name, category, price, stock_quantity)
VALUES
(1, 'Band-Aids', 'First Aid', 1.99, 100),
(2, 'Hand Sanitizer', 'Hygiene', 3.99, 75),
(3, 'Antibiotics', 'Medication', 10.99, 50),
(4, 'Thermometer', 'Medical Devices', 9.99, 30),
(5, 'Pain Relievers', 'Medication', 4.99, 25),
(6, 'Face Masks', 'Hygiene', 0.99, 20),
(7, 'Blood Pressure Monitor', 'Medical Devices', 29.99, 15),
(8, 'Vitamins', 'Supplements', 12.99, 10),
(9, 'Inhaler', 'Medication', 19.99, 50),
(10, 'Gauze Pads', 'First Aid', 2.49, 40);

INSERT INTO Medical_Sales (sale_id, sale_date, item_id, quantity, total_amount)
VALUES
(1, '2023-03-12', 1, 2, 3.98),
(2, '2023-03-12', 3, 1, 10.99),
(3, '2023-03-13', 2, 3, 11.97),
(4, '2023-03-13', 5, 2, 9.98),
(5, '2023-03-14', 8, 1, 12.99),
(6, '2023-03-14', 7, 2, 59.98);

-- Show data from Medical_Items table
SELECT * FROM Medical_Items;

-- Show data from Medical_Sales table
SELECT * FROM Medical_Sales;
