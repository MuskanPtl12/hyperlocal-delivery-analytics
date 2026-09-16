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

# Products Data Modeling

## Final Analytical Schema

| Final Column | Data Type | Business Purpose |
|--------------|-----------|------------------|
| platform | string | Identify the source platform. |
| product_id | string | Unique product identifier. |
| product_name | string | Identify the product. |
| category | string | Category-wise analysis. |
| sub_category | string | Detailed product grouping. |
| brand | string | Brand-wise comparison. |
| price | float64 | Selling price analysis. |
| mrp | float64 | Discount analysis. |
| shelf_life_days | Int64 | Product freshness analysis. |


## Source → Target Transformation

| Final Column | Blinkit | Zepto | Swiggy | ETL Action |
|---------------|----------|--------|---------|------------|
| platform | ❌ | ❌ | ❌ | Add platform name |
| product_id | product_id | product_id | ProductID | Rename `ProductID`, convert to string |
| product_name | product_name | product_name | ProductName | Rename `ProductName` |
| category | category | category | CategoryID | Replace `CategoryID` using Categories table, then standardize values |
| sub_category | NULL | sub_category | NULL | Create business sub-category |
| brand | brand | NULL | NULL | Keep, otherwise NULL |
| price | price | price | UnitPrice | Rename `UnitPrice` |
| mrp | mrp | NULL | NULL | Keep, otherwise NULL |
| shelf_life_days | shelf_life_days | NULL | NULL | Keep, otherwise NULL |
| SupplierID | ❌ | ❌ | SupplierID | Remove (Inventory/Supplier) |
| StockQuantity | ❌ | ❌ | StockQuantity | Remove (Inventory) |
| MinStockLevel | MinStockLevel | ❌ | ❌ | Remove (Inventory) |
| MaxStockLevel | MaxStockLevel | ❌ | ❌ | Remove (Inventory) |
| margin_percentage | margin_percentage | ❌ | ❌ | Exclude (Business meaning not confirmed) |

## Category & Sub-category Standardization

| Final Category | Final Sub-categories |
|----------------|----------------------|
| Fruits & Vegetables | Fruits, Vegetables, Herbs |
| Grocery & Staples | Rice, Flour, Pulses, Edible Oil, Sugar, Salt, Spices, Dry Fruits |
| Dairy & Breakfast | Milk, Curd, Butter & Ghee, Cheese, Bread, Eggs, Breakfast Cereals |
| Snacks & Beverages | Biscuits, Chips, Chocolates, Soft Drinks, Juices, Tea, Coffee |
| Instant & Frozen Foods | Frozen Food, Ready to Cook, Ready to Eat, Instant Noodles |
| Personal Care | Soap & Body Wash, Shampoo, Hair Care, Skin Care, Oral Care, Baby Care |
| Household | Detergent, Dishwash, Floor Cleaner, Toilet Cleaner, Garbage Bags, Air Fresheners, Paper Products |
| Pharmacy & Wellness | Pharmacy & Wellness |
| Pet Care | Pet Care |


### Other

- One row represents one unique product.
- Store unavailable attributes as `NULL`.
- Convert all column names to `snake_case`.
- Remove columns that belong to Inventory or Supplier entities.

### Category Lookup (Swiggy)

- Swiggy Products table stores `CategoryID` instead of `Category Name`.
- Load the `Categories` lookup table before product transformation.
- Join the Products table with the Categories table using `CategoryID`.
- Replace `CategoryID` with the corresponding `Category Name`.
- Remove `CategoryID` after the lookup is completed.
- Perform all further transformations using `Category Name`.

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

### Final Schema

| Final Column | Data Type | Business Purpose |
|---------------|-----------|------------------|
| platform | string | Identify the source platform for cross-platform analysis. |
| delivery_id | string | Unique identifier for each delivery. Store NULL where unavailable. |
| delivery_partner_id | string | Identify the delivery partner responsible for the order. |
| order_id | string | Link delivery records with the Orders table. |
| delivery_time_minutes | Int64 | Measure the total delivery duration from order placement to delivery. |
| distance_km | Float64 | Analyze delivery distance and operational efficiency. |
| delivery_status | string | Track the final delivery status across all platforms. |
| order_status | string | Track order status 
| actual_delivery_datetime | datetime64[ns] | Store the actual delivery time for delivery performance analysis. |
| promised_delivery_datetime | datetime64[ns] | Compare promised vs actual delivery time. |
| delay_reason | string | Analyze reasons for delayed deliveries where available. |


### Source → Target Mapping

| Final Column | Blinkit | Zepto | Swiggy | ETL Action |
|---------------|----------|--------|---------|------------|
| platform | ❌ | ❌ | ❌ | Add platform name |
| delivery_id | NULL | delivery_id | NULL | Keep NULL where unavailable |
| delivery_partner_id | delivery_partner_id | NULL | DeliveryPartnerID | Rename |
| order_id | order_id | order_id | OrderID | Rename |
| delivery_time_minutes | Calculate from Orders + Delivery tables | delivery_time_mins | DeliveryTimeMinutes  | Rename and Recalculate where required |
| distance_km | distance_km | distance_km | NULL | Rename / Keep NULL |
| delivery_status | delivery_status | delivery_status | NULL | Standardize values |
| order_status | NULL | NULL | OrderStatus | Rename|
| actual_delivery_time | actual_time | NULL | DeliveryDate | Rename / and Extract time from delivery_date for swiggy |
| promised_delivery_time | promised_time | NULL | NULL | Rename |
| delay_reason | reasons_if_delayed | NULL | NULL | Rename |


### Business Rules

- Load the **Orders** table where additional delivery information is required.
- Calculate **delivery_time_minutes** using `delivery_time - order_datetime` whenever the source value is missing or represents delay instead of total delivery duration.
- Extract only the **time** component from `DeliveryDate` for Swiggy's `actual_delivery_time`.
- Keep unavailable fields as **NULL (`<NA>`)** instead of generating artificial values.
- Add the `platform` column during ETL.
- Standardize `delivery_status` values across all platforms.
- Validate the final schema, row count, and data types before saving.

**Status:** ✅ Frozen (Version 1)

---

# Customers


### Final Analytical Schema

| Final Column | Data Type | Business Purpose |
|--------------|-----------|------------------|
| platform | string | Identify the source platform for customer analysis. |
| customer_id | string | Identify a customer record within the respective platform. |
| customer_city | string | Geographic customer analysis. |
| customer_state | string | Geographic customer analysis. |
| customer_pincode | Int64 | Pincode-level customer analysis. |
| customer_registration_date | datetime64[ns] | Analyze customer registration trends. |
| customer_segment | string | Customer segmentation analysis. |

---

### Source → Target Transformation

| Final Column | Blinkit | Zepto | Swiggy | ETL Action |
|--------------|----------|-------|--------|------------|
| platform | ❌ | ❌ | ❌ | Add platform name during ETL |
| customer_id | customer_id | customer_id | CustomerID | Rename where required + standardize |
| customer_city | customer_address | city | city | Blinkit: derive city from address; Zepto/Swiggy: rename |
| customer_state | customer_state | state | state | Rename/standardize; NULL where unavailable |
| customer_pincode | pincode | NULL |Pincode| Rename; keep NULL where unavailable |
| customer_registration_date | registration_date | created_date | RegistrationDate | Rename + convert to date datatype |
| customer_segment | customer_segment | NULL | CustomerSegment | Rename + standardize values |

---

#### City Transformation

The city is derived from `customer_address` using the address structure:

- Identify the last address separator (comma or newline).
- Extract the city appearing before the final 6-digit pincode.
- Clean leading/trailing spaces.

#### Customer Segment Standardization

Customer segment values from different platforms are standardized into common analytical values.

| Source Value | Standard Value |
|--------------|----------------|
| Premium | High Value |
| Regular | Frequent Shopper |
| New | New User |
| Lapsed | Inactive |

#### Other

- The final customer table contains only the seven standardized analytical columns.
- Platform information is added during ETL.
- Blinkit city is derived from `customer_address`.
- Common text cleaning is performed after platform-level data is prepared and concatenated.
- Customer segment values are standardized after concatenation.
- Missing attributes are preserved as NULL where the source platform does not provide them.
- Customer registration date is converted to datetime because the source contains date information without a time component.
- No customer-level derived metrics are stored in this table.

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

## Rating 

### Final Analytical Table

Final Schema

| Column Name | Data Type | Description |
|---|---|---|
| `platform` | string | Name of the platform the rating belongs to. |
| `rating_id` | string | Unique identifier for the rating record, where available. |
| `order_id` | string | Identifier of the order associated with the rating, where available. |
| `rating` | float | Numeric customer rating. |
| `feedback` | string | Written customer feedback, where available. |

###  Source-to-Target Mapping

| Final Column | Blinkit    | Zepto      | Instamart | Transformation |
|--------------|----------- |------------|-----------|-----------------|
| `platform`   |   ❌       | ❌        | ❌  | Add platform name during ETL |
| `rating_id`  | feedback ID| rating_id  | NA | Rename to `rating_id` and store as string. |
| `order_id`   | order_id   | order_id   | NA |  store as string. |
| `rating`     | rating_id  | feedback_id| NA| Convert string and Rename |
| `feedback`   | review     | feedback text | NA|  Rename to `feedback` .|

###  Gap Analysis

- Only platforms with available rating data are included.
- Missing source fields are not invented.
- Missing values are retained as nulls where applicable.
- The final table contains only the five agreed columns.


###  Final Decision

- One row represents one customer review for one completed order.
- Reviews from Blinkit and Zepto will be standardized into a single analytical Reviews table.
- Instamart does not provide customer review data, therefore review-related fields will remain NULL.
- Missing attributes will be stored as NULL where unavailable.
