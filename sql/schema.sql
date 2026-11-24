-- ============================================================================
--  Customer RFM & Retention — star schema (SQLite)
--  Grain: one row per invoice line; plus a customer-level RFM table.
-- ============================================================================
DROP TABLE IF EXISTS fact_sale;
DROP TABLE IF EXISTS dim_customer_rfm;
DROP TABLE IF EXISTS dim_customer;
DROP TABLE IF EXISTS dim_product;
DROP TABLE IF EXISTS dim_date;

CREATE TABLE dim_date (
    date_sk     INTEGER PRIMARY KEY,
    invoice_date TEXT UNIQUE,
    year        INTEGER, month INTEGER, month_index INTEGER, month_label TEXT
);
CREATE TABLE dim_customer (
    customer_sk INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL UNIQUE,
    country     TEXT
);
CREATE TABLE dim_product (
    product_sk  INTEGER PRIMARY KEY,
    stock_code  TEXT NOT NULL UNIQUE,
    description TEXT
);
CREATE TABLE dim_customer_rfm (
    customer_sk INTEGER PRIMARY KEY REFERENCES dim_customer(customer_sk),
    recency_days INTEGER, frequency INTEGER, monetary REAL,
    r_score INTEGER, f_score INTEGER, m_score INTEGER,
    segment TEXT, aov REAL, tenure_days INTEGER, first_purchase TEXT, last_purchase TEXT
);
CREATE TABLE fact_sale (
    sale_id     INTEGER PRIMARY KEY,
    invoice     TEXT NOT NULL,
    date_sk     INTEGER REFERENCES dim_date(date_sk),
    customer_sk INTEGER REFERENCES dim_customer(customer_sk),
    product_sk  INTEGER REFERENCES dim_product(product_sk),
    quantity    INTEGER, price REAL, line_total REAL
);
CREATE INDEX idx_sale_customer ON fact_sale(customer_sk);
CREATE INDEX idx_sale_date     ON fact_sale(date_sk);
CREATE INDEX idx_sale_invoice  ON fact_sale(invoice);
