-- Databricks notebook source
-- MAGIC %md
-- MAGIC ## Process Orders Data 
-- MAGIC 1. Ingest the data into the data lakehouse - bronze_orders
-- MAGIC 1. Perform data quality checks and transform the data as required - silver_orders_clean
-- MAGIC 1. Explode the items array from the order object - silver_orders

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### 1. Ingest the data into the data lakehouse - bronze_orders

-- COMMAND ----------

CREATE OR REFRESH STREAMING TABLE bronze_orders
COMMENT "Raw orders data ingested from the source system"
TBLPROPERTIES ("quality" = "bronze")
AS
SELECT *,
        _metadata.file_path AS input_file_path,
       CURRENT_TIMESTAMP AS ingestion_timestamp
  FROM cloud_files(
                    '/Volumes/Circuitbox/Landing/operational_data/Orders/', 
                    'json',
                    map("cloudFiles.inferColumnTypes", "true")
                   );

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### 2. Perform data quality checks and transform the data as required - silver_orders_clean

-- COMMAND ----------

CREATE OR REFRESH STREAMING TABLE silver_orders_clean(
  CONSTRAINT valid_customer_id EXPECT (customer_id IS NOT NULL) ON VIOLATION FAIL UPDATE,
  CONSTRAINT valid_order_id EXPECT (order_id IS NOT NULL) ON VIOLATION FAIL UPDATE,
  CONSTRAINT valid_order_status EXPECT (order_status IN ('Pending', 'Shipped', 'Cancelled', 'Completed')),
  CONSTRAINT valid_payment_method EXPECT (payment_method IN ('Credit Card', 'Bank Transfer', 'PayPal'))
)
COMMENT "Cleaned orders data"
TBLPROPERTIES ("quality" = "silver")
AS
SELECT order_id,
       customer_id,
       CAST(order_timestamp AS TIMESTAMP) AS order_timestamp,
       payment_method,
       items,
       order_status
  FROM STREAM(LIVE.bronze_orders);

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### 3. Explode the items array from the order object - silver_orders

-- COMMAND ----------

CREATE STREAMING TABLE silver_orders
AS
SELECT order_id,
      customer_id,
      order_timestamp,
      payment_method,
      order_status,
      item.item_id,
      item.name AS item_name,
      item.price AS item_price,
      item.quantity AS item_quantity,
      item.category AS item_category
  FROM (SELECT order_id,
              customer_id,
              order_timestamp,
              payment_method,
              order_status,
              explode(items) AS item
          FROM STREAM(LIVE.silver_orders_clean));