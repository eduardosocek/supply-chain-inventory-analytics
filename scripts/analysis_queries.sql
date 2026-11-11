-- ============================================================
-- SUPPLY CHAIN & INVENTORY ANALYTICS - QUERY SUITE
-- ============================================================

-- Query 1: Total Revenue by Product (Shipped & Delivered Orders)
SELECT 
    p.product_id,
    p.product_name,
    p.category,
    SUM(o.quantity_ordered) AS total_units_sold,
    ROUND(SUM(o.quantity_ordered * p.unit_price), 2) AS total_revenue
FROM orders o
INNER JOIN products p 
    ON o.product_id = p.product_id
WHERE o.order_status IN ('Shipped', 'Delivered')
GROUP BY p.product_id, p.product_name, p.category
ORDER BY total_revenue DESC;


-- Query 2: Stockout Risk Alert (Current Inventory vs Safety Stock)
SELECT 
    p.product_id,
    p.product_name,
    i.quantity_on_hand,
    p.safety_stock,
    p.reorder_point,
    CASE 
        WHEN i.quantity_on_hand < p.safety_stock THEN 'CRITICAL'
        WHEN i.quantity_on_hand BETWEEN p.safety_stock AND p.reorder_point THEN 'WARNING'
        ELSE 'OK'
    END AS stock_status
FROM inventory i
INNER JOIN products p 
    ON i.product_id = p.product_id
WHERE i.snapshot_date = (SELECT MAX(snapshot_date) FROM inventory)
ORDER BY i.quantity_on_hand ASC;
