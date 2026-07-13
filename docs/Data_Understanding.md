# Data Understanding

This project uses multiple datasets collected from Kaggle to simulate the operational data of India's leading quick-commerce platforms. Since real company databases are private and cannot be accessed publicly, publicly available datasets are used to recreate a real-world business analytics environment.

The project focuses on comparing the performance of the following platforms:

- Blinkit
- Zepto
- Swiggy Instamart
- BigBasket
- JioMart (via cross-platform dataset)

The collected datasets contain information related to customer orders, products, inventory, delivery operations, customer feedback, ratings, marketing campaigns, and transactions.


## 2. Selected Datasets

| `Platform` | `Dataset` | `Purpose` | `Status`| `Tables Used`|
|----------|----------|----------|---------|-------------------------------------------|
| Blinkit | Blinkit Sales Dataset | Core Dataset | ✅ Selected |9|
| Zepto | Zepto Online Grocery & Delivery Dataset | Core Dataset | ✅ Selected |7|
| Swiggy Instamart | Swiggy Instamart Dataset | Core Dataset | ✅ Selected |8|
| BigBasket | BigBasket Products Dataset | Supporting Dataset | ✅ Selected |1|
|jiomart| Quick Commerce Orders Dataset | supporting Dataset |  ✅ Selected |1|
| Cross Platform | Quick Commerce Orders Dataset | Cross-Platform Comparison | ✅ Selected |1|

---
Total Tables Used: 26

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


## Blinkit 

| `Table`              | `Rows`| `Columns` | `PK `     | `FK`                | `Domain`  |`Decision`   |
| -------------------- | ----- | ------- | ----------- | ------------------- | --------- | ---------   |
| Orders               | 5000  | 10      | order_id    | customer_id         | Delivery  | ✅         |
| Customers            | 2500  | 11      | customer_id | -                   | Customer  | ✅         |
| Products             | 268   | 10      | product_id  | -                   | Inventory | ✅         |
| Inventory            | 75000 | 4       | product_id  | -                   | Inventory | ✅         |
| Delivery Performance | 5000  | 8       | order_id    | delivery_partner_id | Delivery  | ✅         |
| Customer Feedback    | 5000  | 8       | feedback_id | order_id            | Customer  | ✅         |
| Marketing            | 5400  | 11      | campaign_id | -                   | Marketing | 🔄 Future |


### Key Observations

- Date columns are stored as string.
- Primary and foreign keys identified.
- Marketing dataset will be used in Phase 2.
- InventoryNew requires validation.
- delivery_status in order table `['On Time', 'Slightly Delayed', 'Significantly Delayed']` is different meaning from delivery table's delivery_status `['Delivered Late', 'Delivered On Time']`.
- Need to convert delivery_status in order table into order_status.

### Cleaning Notes

- Convert date columns to `datetime`
- Validate primary key uniqueness



## Zepto 
 

| `Table`              | `Rows`| `Columns`| `PK `         | `FK`                | `Domain`    |`Decision`   |
| -------------------- | ----- | -------  | -----------   | ------------------- | ---------   | ---------   |
| Orders               | 20,000| 4        | order_id      | customer_id         | Delivery    | ✅         |
| Customers            | 10,000| 8        | customer_id   | -                   | Customer    | ✅         |
| Products             | 1200  | 5        | product_id    | -                   | Inventory   | ✅         |
| Delivery             | 20,000| 5        | delivery_id   | order_id            | Delivery    | ✅         |
| Rating               | 20,000| 4        | rating_id     | order_id            | Customer    | ✅         |
|Transaction           | 50,000| 6        | transaction_id| order_id,product_id | Marketing   | ✅         |

### Key Observations

- Date columns are stored as string.
- Primary and foreign keys identified.
- order_id, customer_id , product_id , transaction_id, rating_id , delivery_id  all columns are in string datatype.
- order_id are not same in other table (`delivery , rating , transcation`), 5000,7000 are not exist .
- missing 5000 order_id in rating table and transaction table are same .

### Cleaning Notes

- Convert date columns to `datetime`
- Convert order_id, customer_id , product_id , transaction_id, rating_id , delivery_id  all columns are into `Int`
- Validate primary key uniqueness
- Standardize column names and data value