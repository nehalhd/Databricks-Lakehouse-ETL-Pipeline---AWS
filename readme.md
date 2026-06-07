# CircuitBox Lakehouse ETL Pipeline
### Databricks Lakeflow | Delta Live Tables (DLT) | Unity Catalog | AWS S3

---

## Project Overview

CircuitBox is an end-to-end Data Engineering project designed to demonstrate the implementation of a modern Lakehouse architecture using Databricks, Delta Lake, Unity Catalog, and AWS S3.

The project follows the Medallion Architecture (Bronze, Silver, and Gold layers) and utilizes Delta Live Tables (DLT) pipelines to automate data ingestion, transformation, quality validation, and business-level aggregations.

The solution ingests operational data from AWS S3, processes it through multiple layers, and delivers analytics-ready datasets for reporting and AI/ML workloads.

---

# Architecture Overview

## Technologies Used

| Technology | Purpose |
|------------|----------|
| Databricks | Data Engineering Platform |
| Delta Lake | ACID Transactions & Storage Format |
| Delta Live Tables (DLT) | Pipeline Orchestration |
| Lakeflow Pipelines | Incremental Processing |
| Unity Catalog | Governance & Metadata Management |
| AWS S3 | Data Storage |
| Auto Loader | Incremental File Ingestion |
| SQL | Data Transformation |
| Serverless Compute | Pipeline Execution |

---

# Data Architecture

## AWS S3 Storage Layer

The source data is stored in an AWS S3 bucket.

### S3 Structure

```text
s3://circuitbox
│
└── operational_data
    ├── customers.json
    ├── addresses.csv
    └── orders.json
```

---

## Unity Catalog Structure

```text
UC Metastore
│
└── Catalog: circuitbox
    │
    ├── Schema: landing
    │   └── Volume: operational_data
    │
    └── Schema: lakehouse
        ├── Bronze Tables
        ├── Silver Tables
        └── Gold Tables
```

---

## Governance Components

The project leverages Unity Catalog for centralized governance.

### Governance Features

- Access Control
- Data Lineage
- Auditability
- Metadata Management
- Data Discovery
- Catalog Organization

---

# Data Pipeline Architecture

The project follows the Medallion Architecture.

```text
Landing
   ↓
Bronze
   ↓
Silver Clean
   ↓
Silver Business
   ↓
Gold
   ↓
BI & Analytics
```

---

# Landing Layer

The Landing Layer stores raw operational files inside a Unity Catalog Volume.

### Source Datasets

| Dataset | Format |
|----------|----------|
| Customers | JSON |
| Addresses | CSV |
| Orders | JSON |

---

# Bronze Layer

## Purpose

The Bronze Layer stores raw ingested data exactly as received from source systems.

### Ingestion Method

- Auto Loader
- Incremental Processing
- Delta Format Storage

### Bronze Tables

#### Bronze_Customers

Source:

```text
customers.json
```

#### Bronze_Addresses

Source:

```text
addresses.csv
```

#### Bronze_Orders

Source:

```text
orders.json
```

---

# Silver Layer

The Silver Layer applies data quality validation, cleansing, and business transformations.

---

## Data Quality Validation

DLT Expectations are used to enforce quality rules.

### Examples

#### Customer Rules

- Customer ID must not be null
- Customer Name must not be null
- Telephone must be valid

#### Address Rules

- Address fields must be populated
- State values must be valid

#### Order Rules

- Order ID must exist
- Payment information must be valid

---

## Silver Clean Tables

### Silver_Customers_Clean

Validated customer records.

---

### Silver_Addresses_Clean

Validated address records.

---

### Silver_Orders_Clean

Validated order records.

---

## Business Transformation Tables

### Silver_Customers

Purpose:

Store the latest customer attributes.

Implementation:

```text
SCD Type 1
```

Characteristics:

- Updates overwrite existing records.
- Only latest version is maintained.

---

### Silver_Addresses

Purpose:

Track historical customer address changes.

Implementation:

```text
SCD Type 2
```

Characteristics:

- Historical records preserved.
- Full address change tracking.
- Effective dating support.

---

### Silver_Orders

Purpose:

Flatten nested order structures.

Transformation:

```text
EXPLODE
```

Characteristics:

- Converts nested arrays into row-level records.
- Simplifies reporting and aggregation.

---

# Gold Layer

The Gold Layer contains business-ready datasets optimized for analytics and reporting.

---

## Gold_Customer_Order_Summary

This table combines customer, address, and order information into a single analytical dataset.

### Data Sources

```text
Silver_Customers
+
Silver_Addresses
+
Silver_Orders
```

---

## Business Metrics

The Gold table provides:

- Total Orders
- Total Items Ordered
- Total Order Amount
- Customer Information
- Latest Customer Address

---

## Business Value

The Gold layer enables:

- Customer Analytics
- Sales Reporting
- Order Trend Analysis
- Executive Dashboards
- AI/ML Feature Engineering

---

# Analytics & Reporting

The Gold dataset is consumed by:

### BI Dashboards

- Sales Dashboard
- Customer Dashboard
- Executive Dashboard

### Reports

- Customer Order Summary
- Revenue Analysis
- Order Statistics

### AI / ML Workloads

- Customer Segmentation
- Purchase Prediction
- Recommendation Systems

---

# Data Governance

The project uses Unity Catalog to implement governance controls.

---

## Access Control

Data access can be managed through Unity Catalog permissions.

---

## Data Lineage

Unity Catalog provides end-to-end lineage visibility.

Example:

```text
customers.json
↓
Bronze_Customers
↓
Silver_Customers_Clean
↓
Silver_Customers
↓
Gold_Customer_Order_Summary
```

---

## Auditability

All operations can be monitored and audited through Databricks.

---

## Data Discovery

Catalogs, schemas, and tables are searchable through Unity Catalog.

---

# Platform Services

## Delta Lake

Provides:

- ACID Transactions
- Schema Enforcement
- Time Travel
- Version Control

---

## Delta Live Tables (DLT)

Provides:

- Pipeline Automation
- Dependency Management
- Data Quality Enforcement
- Incremental Processing

---

## Serverless Compute

Provides:

- Automatic Scaling
- Reduced Operational Overhead
- Cost Optimization

---

# Pipeline Flow Summary

```text
AWS S3
│
├── customers.json
├── addresses.csv
└── orders.json
        │
        ▼
Landing Volume
        │
        ▼
Auto Loader
        │
        ▼
Bronze Layer
        │
        ▼
Silver Clean Layer
        │
        ▼
Business Transformations
│
├── SCD Type 1
├── SCD Type 2
└── Explode
        │
        ▼
Gold_Customer_Order_Summary
        │
        ▼
BI Dashboards
Reports
AI/ML
```

---

# Key Features

- End-to-End Lakehouse Architecture
- AWS S3 Integration
- Auto Loader Incremental Ingestion
- Delta Live Tables (DLT)
- Data Quality Expectations
- SCD Type 1 Implementation
- SCD Type 2 Implementation
- Nested Data Explode Transformations
- Gold Business Aggregations
- Unity Catalog Governance
- Data Lineage & Auditability
- Serverless Pipeline Execution

---

