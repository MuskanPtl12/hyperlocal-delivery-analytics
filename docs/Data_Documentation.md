# Data Documentation

## 1. Dataset Overview

This project uses multiple datasets collected from Kaggle to simulate the operational data of India's leading quick-commerce platforms. Since real company databases are private and cannot be accessed publicly, publicly available datasets are used to recreate a real-world business analytics environment.

The project focuses on comparing the performance of the following platforms:

- Blinkit
- Zepto
- Swiggy Instamart
- BigBasket
- JioMart (via cross-platform dataset)

The collected datasets contain information related to customer orders, products, inventory, delivery operations, customer feedback, ratings, marketing campaigns, and transactions.

---

## 2. Selected Datasets

| Platform | Dataset | Purpose | Status |
|----------|----------|----------|---------|
| Blinkit | Blinkit Sales Dataset | Core Dataset | ✅ Selected |
| Zepto | Zepto Online Grocery & Delivery Dataset | Core Dataset | ✅ Selected |
| Instamart | Swiggy Instamart Dataset | Core Dataset | ✅ Selected |
| BigBasket | BigBasket Products Dataset | Supporting Dataset | ✅ Selected |
| Cross Platform | Quick Commerce Orders Dataset | Cross-Platform Comparison | ✅ Selected |

---

## 3. Dataset Purpose

### Blinkit Sales Dataset (Core Dataset)

This dataset provides a complete operational view of Blinkit's business, including customers, orders, products, inventory, delivery performance, customer feedback, and marketing campaigns. It serves as the primary dataset for analyzing delivery operations, inventory management, and customer experience.

---

### Zepto Online Grocery & Delivery Dataset (Core Dataset)

This dataset contains customer, order, transaction, delivery, product, and rating information. It is used to analyze customer purchasing behavior, delivery efficiency, product demand, and inventory performance.

---

### Swiggy Instamart Dataset (Core Dataset)

This dataset includes customer details, addresses, products, delivery partners, and order transactions. It helps evaluate delivery operations, logistics performance, and order fulfillment across different locations.

---

### BigBasket Products Dataset (Supporting Dataset)

This dataset mainly contains product-related information such as product name, brand, category, quantity, and pricing details. It will be used as a supporting product master dataset for product comparison, category analysis, and pricing insights.

---

### Quick Commerce Orders Dataset (Cross-Platform Dataset)

This dataset combines order information from multiple quick-commerce platforms, including Blinkit, Swiggy Instamart, and JioMart. It provides a standardized dataset for comparing platform performance, delivery delays, customer ratings, refund requests, and overall operational efficiency.

---

## 4. Data Source Strategy

| Data Type | Source | Type |
|-----------|--------|------|
| Orders | Kaggle Datasets | Historical |
| Customers | Kaggle Datasets | Historical |
| Products | Kaggle Datasets | Historical |
| Inventory | Kaggle Datasets | Historical |
| Customer Reviews | Kaggle Datasets | Historical |
| Weather Data | Weather API *(Future)* | Real-Time |
| Bangalore Pincode Data | Government/Open Data *(Future)* | Reference Data |
| Traffic Data | Traffic API *(Future)* | Real-Time |

---

## 5. Current Project Status

| Task | Status |
|------|--------|
| Business Understanding | ✅ Completed |
| Business Questions Finalized | ✅ Completed |
| Dataset Research | ✅ Completed |
| Dataset Selection | ✅ Completed |
| Project Setup | ✅ Completed |
| GitHub Repository | ✅ Completed |
| VS Code Setup | ✅ Completed |
| Virtual Environment | ✅ Completed |
| Data Understanding | 🔄 In Progress |
| Data Modeling | ⏳ Pending |
| ETL Development | ⏳ Pending |
| Data Analysis | ⏳ Pending |
| Dashboard Development | ⏳ Pending |