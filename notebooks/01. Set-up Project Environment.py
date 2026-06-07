# Databricks notebook source
# MAGIC %md
# MAGIC %md
# MAGIC ## Set-up the project environment for CircuitBox Data Lakehouse
# MAGIC 1. Create external location - circuitbox_ext_loc
# MAGIC 1. Create Catalog - circuitbox
# MAGIC 1. Create Schemas
# MAGIC     - landing
# MAGIC     - lakehouse
# MAGIC 1. Create Volume - operational_data

# COMMAND ----------

# MAGIC %md
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ###1. Create External Location
# MAGIC External Location Name: circuitbox_ext_loc
# MAGIC
# MAGIC S3 Path: s3://databricks-otdpcxq6gpbrynrrsk6i4b-cloud-storage-bucket/CircuitBox/
# MAGIC
# MAGIC Storage Credential: IAM Role : s3-role

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE EXTERNAL LOCATION IF NOT EXISTS circuitbox_ext_loc
# MAGIC   URL 's3://databricks-otdpcxq6gpbrynrrsk6i4b-cloud-storage-bucket/CircuitBox/'
# MAGIC   WITH (STORAGE CREDENTIAL s3-role)
# MAGIC   COMMENT 'External Location for the circuitbox data lakehouse';

# COMMAND ----------

# MAGIC %md
# MAGIC ###2. Create catalog
# MAGIC
# MAGIC **Catalog Name**: circuitbox
# MAGIC
# MAGIC **Managed Location**: 's3://databricks-otdpcxq6gpbrynrrsk6i4b-cloud-storage-bucket/CircuitBox/'

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE CATALOG IF NOT EXISTS circuitbox
# MAGIC MANAGED LOCATION 's3://databricks-otdpcxq6gpbrynrrsk6i4b-cloud-storage-bucket/CircuitBox/'
# MAGIC COMMENT 'Catalog for the circuitbox data lakehouse';

# COMMAND ----------

# MAGIC %md
# MAGIC **Show Catalogs:**

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW CATALOGS;

# COMMAND ----------

# MAGIC %md
# MAGIC ###3. Create Schemas
# MAGIC **Schema Name**: landing
# MAGIC
# MAGIC **Managed Location**: s3://databricks-otdpcxq6gpbrynrrsk6i4b-cloud-storage-bucket/CircuitBox/Landing/
# MAGIC
# MAGIC **Schema Name**: lakehouse
# MAGIC
# MAGIC **Managed Location**: s3://databricks-otdpcxq6gpbrynrrsk6i4b-cloud-storage-bucket/CircuitBox/Lakehouse/

# COMMAND ----------

# MAGIC %sql
# MAGIC USE CATALOG circuitbox;
# MAGIC
# MAGIC CREATE SCHEMA IF NOT EXISTS landing
# MAGIC    MANAGED LOCATION 's3://databricks-otdpcxq6gpbrynrrsk6i4b-cloud-storage-bucket/CircuitBox/Landing/';
# MAGIC CREATE SCHEMA IF NOT EXISTS lakehouse
# MAGIC    MANAGED LOCATION 's3://databricks-otdpcxq6gpbrynrrsk6i4b-cloud-storage-bucket/CircuitBox/Lakehouse/';

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW SCHEMAS;
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ###4. Create Volume
# MAGIC
# MAGIC **Volume Name**: operational_data
# MAGIC
# MAGIC **S3 Path**: s3://databricks-otdpcxq6gpbrynrrsk6i4b-cloud-storage-bucket/CircuitBox/Landing/operational_data/

# COMMAND ----------

# MAGIC %sql
# MAGIC USE CATALOG circuitbox;
# MAGIC USE SCHEMA landing;
# MAGIC
# MAGIC CREATE EXTERNAL VOLUME IF NOT EXISTS operational_data
# MAGIC       LOCATION 's3://databricks-otdpcxq6gpbrynrrsk6i4b-cloud-storage-bucket/CircuitBox/Landing/operational_data/';

# COMMAND ----------

# MAGIC
# MAGIC %fs ls /Volumes/circuitbox/landing/operational_data