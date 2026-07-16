# Data Model

## Objective

The objective of this document is to design a common analytical data model for integrating multiple quick-commerce platforms into a standardized structure.

The data model will serve as the blueprint for the ETL pipeline and define:

- Final analytical tables
- Standardized column names
- Source-to-target mapping
- Gap analysis
- Table relationships

---

# Orders

### Final Analytical Table

| Final Column | Source Platform | Business Purpose |
|---------------|----------------|------------------|
| platform | All | Identify the source platform for cross-platform comparison. |
| order_id | All | Unique identifier for each order. |
| customer_id | Blinkit, Zepto, Instamart | Identify the customer who placed the order. |
| order_datetime | All | Analyze peak hours, daily, weekly and monthly order trends. |
| promised_delivery_datetime | Blinkit | Measure promised delivery SLA. |
| actual_delivery_datetime | Blinkit, Instamart | Measure actual delivery performance. |
| delivery_status | All | Identify delivered, delayed, cancelled and failed orders. |
| order_value | Blinkit, Instamart | Revenue and Average Order Value (AOV) analysis. |
| payment_method | Blinkit, Instamart | Future customer payment behaviour analysis. |
| warehouse_id | Blinkit (Store ID), Instamart (StoreID) | Link orders to warehouses/dark stores. |
| customer_pincode | Blinkit | Hyperlocal and Bangalore area analysis. |


### Source-to-Target Mapping

| Final Column | Blinkit | Zepto | Instamart | Transformation |
|---------------|----------|--------|------------|----------------|
| platform | ❌ | ❌ | ❌ | Add platform name during ETL |
| order_id | order_id | order_id | OrderID | Rename |
| customer_id | customer_id | customer_id | CustomerID | Rename |
| order_datetime | order_date | order_date | OrderDate | Rename + Convert to datetime |
| promised_delivery_datetime | promised_delivery_time | NULL | NULL | Keep NULL if unavailable |
| actual_delivery_datetime | actual_delivery_time | NULL | DeliveryDate | Rename + Convert to datetime |
| delivery_status | delivery_status | order_status | OrderStatus | Standardize values |
| order_value | order_total | NULL | TotalPrice | Rename |
| payment_method | payment_method | NULL | PaymentMethodID | Standardize |
| warehouse_id | store_id | NULL | StoreID | Rename |
| customer_pincode | Available | NULL | NULL | Keep NULL if unavailable |


### Gap Analysis

| Missing Information | Platform | Decision |
|---------------------|----------|----------|
| Promised Delivery Time | Zepto, Instamart | Store as NULL |
| Actual Delivery Time | Zepto | Store as NULL |
| Order Value | Zepto | Store as NULL |
| Payment Method | Zepto | Store as NULL |
| Customer Pincode | Zepto, Instamart | Store as NULL |
| Warehouse ID | Zepto | Store as NULL |


## Final Decision

- One row represents one customer order.
- Orders from all platforms will be standardized into a single analytical Orders table.
- Missing attributes will be stored as NULL where the source platform does not provide them.
- This table is **Frozen (Version 1)** and will be used during the ETL phase.

---

# Products

### Final Analytical Table

| Final Column | Source Platform | Business Purpose |
|---------------|----------------|------------------|
| platform | All | Identify the source platform for cross-platform comparison. |
| product_id | All | Unique identifier for each product. |
| product_name | All | Identify and compare products across platforms. |
| category | All | Analyze product demand and category-wise sales performance. |
| sub_category | Zepto, Instamart | Perform detailed product category analysis. |
| brand | Blinkit | Compare branded and non-branded products across platforms. |
| price | All | Analyze pricing differences across platforms. |
| mrp | Blinkit | Measure discounts and customer savings. |
| stock_quantity | Instamart | Monitor inventory availability and stock levels. |
| reorder_level | Blinkit | Identify products requiring replenishment before stock-out. |
| shelf_life_days | Blinkit | Support product freshness and expiry analysis. |


### Source-to-Target Mapping

| Final Column | Blinkit | Zepto | Instamart | Transformation |
|---------------|----------|--------|------------|----------------|
| platform | ❌ | ❌ | ❌ | Add platform name during ETL |
| product_id | product_id | product_id | ProductID | Rename |
| product_name | product_name | product_name | ProductName | Rename |
| category | category | category | CategoryID | Replace CategoryID with Category Name using Categories table |
| sub_category | NULL | sub_category | NULL | Keep NULL where unavailable |
| brand | brand | NULL | NULL | Keep NULL where unavailable |
| price | price | price | UnitPrice | Rename |
| mrp | mrp | NULL | NULL | Keep NULL where unavailable |
| stock_quantity | NULL | NULL | StockQuantity | Rename |
| reorder_level | min_stock_level | NULL | NULL | Rename |
| shelf_life_days | shelf_life_days | NULL | NULL | Rename |


### Gap Analysis

| Missing Information | Platform | Decision |
|---------------------|----------|----------|
| Brand | Zepto, Instamart | Store as NULL |
| MRP | Zepto, Instamart | Store as NULL |
| Stock Quantity | Blinkit, Zepto | Store as NULL |
| Shelf Life | Zepto, Instamart | Store as NULL |
| Reorder Level | Zepto, Instamart | Store as NULL |
| Sub Category | Blinkit, Instamart | Store as NULL |


### Final Decision

- One row represents one unique product.
- Products from all supported platforms will be standardized into a single analytical Products table.
- Category IDs will be replaced with category names during ETL wherever lookup tables are available.
- Missing attributes will be stored as NULL if the source platform does not provide them.
- **Status:** ✅ Frozen (Version 1)

---

# Transaction

### Final Analytical Table

| Final Column | Source Platform | Business Purpose |
|---------------|----------------|------------------|
| platform | All | Identify the source platform for cross-platform analysis. |
| transaction_id | Zepto | Unique identifier for each transaction (NULL or generated where unavailable). |
| order_id | All | Link transaction to the Orders table. |
| product_id | All | Link transaction to the Products table. |
| quantity | All | Analyze product demand and quantity sold. |
| unit_price | Blinkit | Calculate product pricing and revenue metrics. |
| total_amount | Zepto, Instamart | Measure revenue generated by each transaction. |
| payment_method | Blinkit, Zepto, Instamart | Analyze customer payment preferences. |
| discount_amount | Instamart | Analyze discount impact on sales. |


### Source-to-Target Mapping

| Final Column | Blinkit | Zepto | Instamart | Transformation |
|---------------|----------|--------|------------|----------------|
| platform | ❌ | ❌ | ❌ | Add platform name during ETL |
| transaction_id | NULL | transaction_id | NULL | Generate or keep NULL |
| order_id | order_id | order_id | OrderID | Rename |
| product_id | product_id | product_id | ProductID | Rename |
| quantity | quantity | quantity | Quantity | Rename |
| unit_price | unit_price | NULL | Calculate or NULL | Rename |
| total_amount | Join from Orders (order_total) | amount | TotalPrice | Rename / Join |
| payment_method | Join from Orders | payment_mode | PaymentMethodID | Rename / Join |
| discount_amount | NULL | NULL | DiscountApplied | Rename |


### Gap Analysis

| Missing Information | Platform | Decision |
|---------------------|----------|----------|
| Transaction ID | Blinkit, Instamart | Generate during ETL or keep NULL |
| Unit Price | Zepto, Instamart | Store NULL or calculate where possible |
| Total Amount | Blinkit | Join with Orders table |
| Payment Method | Blinkit | Join with Orders table |
| Discount Amount | Blinkit, Zepto | Store NULL |


### Final Decision

- One row represents one product purchased within one customer order.
- The Transaction table acts as the bridge between Orders and Products.
- Missing attributes will be stored as NULL or generated during ETL where appropriate.
- Status: ✅ Frozen (Version 1)

---

# Delivery

### Final Analytical Table

| Final Column | Source Platform | Business Purpose |
|---------------|----------------|------------------|
| platform | All | Identify the source platform for cross-platform delivery comparison. |
| delivery_id | Zepto | Unique identifier for each delivery (NULL where unavailable). |
| order_id | All | Link delivery information to the Orders table. |
| delivery_partner_id | Blinkit, Instamart | Identify the delivery partner/rider responsible for the delivery. |
| promised_delivery_time | Blinkit | Measure SLA (promised delivery commitment). |
| actual_delivery_time | Blinkit, Instamart | Measure actual delivery completion time. |
| delivery_time_minutes | All | Analyze delivery efficiency and average delivery time. |
| distance_km | Blinkit, Zepto | Analyze the impact of distance on delivery performance. |
| delivery_status | All | Identify successful, delayed, cancelled, or failed deliveries. |
| delay_reason | Blinkit | Identify operational reasons for delayed deliveries. |


### Source-to-Target Mapping

| Final Column | Blinkit | Zepto | Instamart | Transformation |
|---------------|----------|--------|------------|----------------|
| platform | ❌ | ❌ | ❌ | Add platform name during ETL |
| delivery_id | NULL | delivery_id | NULL | Keep NULL where unavailable |
| order_id | order_id | order_id | OrderID | Rename |
| delivery_partner_id | delivery_partner_id | NULL | DeliveryPartnerID | Rename |
| promised_delivery_time | promised_time | NULL | NULL | Rename |
| actual_delivery_time | actual_time | NULL | DeliveryDate | Rename + Convert to datetime |
| delivery_time_minutes | delivery_time_minutes | delivery_time_mins | DeliveryTimeMinutes | Rename |
| distance_km | distance_km | distance_km | NULL | Rename |
| delivery_status | delivery_status | delivery_status | OrderStatus | Standardize values |
| delay_reason | reasons_if_delayed | NULL | NULL | Rename |

### Gap Analysis

| Missing Information | Platform | Decision |
|---------------------|----------|----------|
| Delivery ID | Blinkit, Instamart | Store NULL |
| Delivery Partner | Zepto | Store NULL |
| Promised Delivery Time | Zepto, Instamart | Store NULL |
| Actual Delivery Time | Zepto | Store NULL |
| Distance | Instamart | Store NULL |
| Delay Reason | Zepto, Instamart | Store NULL |


### Final Decision

- One row represents one delivery associated with one customer order.
- Delivery information from Blinkit, Zepto, and Instamart will be standardized into a single analytical Delivery table.
- Missing attributes will be stored as NULL where the source platform does not provide them.
- The Quick Commerce dataset will **not** be used to fill missing delivery information because it has independent identifiers and cannot be reliably joined.
- **Status:** ✅ Frozen (Version 1)
---

# Customers

### Final Analytical Table

| Final Column | Source Platform | Business Purpose |
|---------------|----------------|------------------|
| platform | All | Identify the source platform for cross-platform customer analysis. |
| customer_id | All | Unique identifier for each customer. |
| customer_name | All | Identify individual customers. |
| email | All | Customer contact information. |
| phone | Blinkit, Instamart | Customer contact information. |
| gender | Zepto | Customer demographic analysis. |
| age | Zepto | Customer demographic analysis. |
| city | Zepto | Geographic customer analysis. |
| state | Zepto | Geographic customer analysis. |
| area | Blinkit | Hyperlocal customer analysis. |
| pincode | Blinkit | Bangalore pincode-wise customer analysis. |
| registration_date | All | Analyze customer acquisition trends. |
| customer_segment | Blinkit, Instamart | Customer segmentation analysis. |


### Source-to-Target Mapping

| Final Column | Blinkit | Zepto | Instamart | Transformation |
|---------------|----------|--------|------------|----------------|
| platform | ❌ | ❌ | ❌ | Add platform name during ETL |
| customer_id | customer_id | customer_id | CustomerID | Rename |
| customer_name | customer_name | customer_name | CustomerName | Rename |
| email | email | email | Email | Rename |
| phone | phone | NULL | phone | Rename |
| gender | NULL | gender | NULL | Keep NULL where unavailable |
| age | NULL | age | NULL | Keep NULL where unavailable |
| city | NULL | city | NULL | Keep NULL where unavailable |
| state | NULL | state | NULL | Keep NULL where unavailable |
| area | area | NULL | NULL | Keep NULL where unavailable |
| pincode | pincode | NULL | NULL | Keep NULL where unavailable |
| registration_date | registration_date | created_date | RegistrationDate | Rename + Convert to datetime |
| customer_segment | customer_segment | NULL | CustomerSegment | Rename |


### Gap Analysis

| Missing Information | Platform | Decision |
|---------------------|----------|----------|
| Phone | Zepto | Store NULL |
| Gender | Blinkit, Instamart | Store NULL |
| Age | Blinkit, Instamart | Store NULL |
| City | Blinkit, Instamart | Store NULL |
| State | Blinkit, Instamart | Store NULL |
| Area | Zepto, Instamart | Store NULL |
| Pincode | Zepto, Instamart | Store NULL |
| Customer Segment | Zepto | Store NULL |


### Final Decision

- One row represents one unique customer.
- Customer information from all platforms will be standardized into a single analytical Customers table.
- Derived attributes such as **Total Orders** and **Average Order Value** will not be stored because they can be calculated from the Orders table.
- Missing attributes will be stored as NULL where the source platform does not provide them.
- **Status:** ✅ Frozen (Version 1)

---

# Inventory

### Final Analytical Table

| Final Column | Source Platform | Business Purpose |
|---------------|----------------|------------------|
| platform | All | Identify the source platform for inventory comparison. |
| product_id | All | Link inventory to the Products table. |
| inventory_date | Blinkit | Analyze daily inventory movement and trends. |
| stock_quantity | Instamart | Measure current stock availability. |
| available_quantity | Zepto | Monitor available inventory for customer orders. |
| stock_received | Blinkit | Analyze stock replenishment over time. |
| damaged_stock | Blinkit | Measure inventory loss due to damaged products. |
| reorder_level | Blinkit | Identify products that require replenishment. |
| stock_status | Zepto | Identify products that are in stock or out of stock. |

### Source-to-Target Mapping

| Final Column | Blinkit | Zepto | Instamart | Transformation |
|---------------|----------|--------|------------|----------------|
| platform | ❌ | ❌ | ❌ | Add platform name during ETL |
| product_id | product_id | product_id | ProductID | Rename |
| inventory_date | date | NULL | NULL | Rename + Convert to datetime |
| stock_quantity | NULL | quantity | StockQuantity | Rename |
| available_quantity | NULL | availableQuantity | NULL | Rename |
| stock_received | stock_received | NULL | NULL | Rename |
| damaged_stock | damaged_stock | NULL | NULL | Rename |
| reorder_level | min_stock_level (Products Table) | NULL | NULL | Join Products table |
| stock_status | NULL | outOfStock | NULL | Convert Boolean to In Stock / Out of Stock |


### Gap Analysis

| Missing Information | Platform | Decision |
|---------------------|----------|----------|
| Inventory Date | Zepto, Instamart | Store NULL |
| Stock Received | Zepto, Instamart | Store NULL |
| Damaged Stock | Zepto, Instamart | Store NULL |
| Reorder Level | Zepto, Instamart | Store NULL |
| Available Quantity | Blinkit, Instamart | Store NULL |
| Stock Status | Blinkit, Instamart | Store NULL |

### Final Decision

- One row represents the inventory status of one product.
- Inventory information from Blinkit, Zepto, and Instamart will be standardized into a single analytical Inventory table.
- Inventory movement (stock received, damaged stock) and inventory status (stock quantity, available quantity, stock status) will coexist because different platforms provide different inventory details.
- Missing attributes will be stored as NULL where unavailable.
- **Status:** ✅ Frozen (Version 1)

---

# Reviews

### Final Analytical Table

| Final Column | Source Platform | Business Purpose |
|---------------|----------------|------------------|
| platform | All | Identify the source platform for customer review analysis. |
| review_id | Blinkit, Zepto | Unique identifier for each review. |
| order_id | Blinkit, Zepto | Link reviews to the Orders table. |
| customer_id | Blinkit | Link reviews to the Customers table. |
| rating | Blinkit, Zepto | Measure customer satisfaction. |
| review_text | Blinkit, Zepto | Perform customer sentiment and text analysis. |
| feedback_category | Blinkit | Categorize customer issues and compliments. |
| sentiment | Blinkit | Analyze positive, neutral, and negative customer feedback. |
| review_date | Blinkit | Analyze review trends over time. |


### Source-to-Target Mapping

| Final Column | Blinkit | Zepto | Instamart | Transformation |
|---------------|----------|--------|------------|----------------|
| platform | ❌ | ❌ | ❌ | Add platform name during ETL |
| review_id | feedback_id | rating_id | NULL | Rename |
| order_id | order_id | order_id | NULL | Rename |
| customer_id | customer_id | NULL | NULL | Keep NULL where unavailable |
| rating | rating | rating | NULL | Rename |
| review_text | feedback_text | review | NULL | Rename |
| feedback_category | feedback_category | NULL | NULL | Rename |
| sentiment | sentiment | NULL | NULL | Rename |
| review_date | feedback_date | NULL | NULL | Rename + Convert to datetime |


### Gap Analysis

| Missing Information | Platform | Decision |
|---------------------|----------|----------|
| Customer ID | Zepto | Store NULL |
| Feedback Category | Zepto, Instamart | Store NULL |
| Sentiment | Zepto, Instamart | Store NULL |
| Review Date | Zepto, Instamart | Store NULL |
| Complete Review Dataset | Instamart | Store NULL |


###  Final Decision

- One row represents one customer review for one completed order.
- Reviews from Blinkit and Zepto will be standardized into a single analytical Reviews table.
- Instamart does not provide customer review data, therefore review-related fields will remain NULL.
- Missing attributes will be stored as NULL where unavailable.
- **Status:** ✅ Frozen (Version 1)