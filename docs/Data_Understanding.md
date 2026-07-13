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


## Blinkit 

| `Table`              | `Rows`| `Columns` | `PK `     | `FK`                | `Domain`  |`Decision`   |
| -------------------- | ----- | ------- | ----------- | ------------------- | --------- | ---------   |
| Orders1              | 5000  | 10      | order_id    |customer_id,delivery_partner_id | Delivery  | ✅    |
| Orders2              | 5000  | 4       | order_id    |product_id           | Delivery  | ✅         |
| Customers            | 2500  | 11      | customer_id | -                   | Customer  | ✅         |
| Products             | 268   | 10      | product_id  | -                   | Inventory | ✅         |
| Inventory            | 75000 | 4       | product_id  | -                   | Inventory | ✅         |
| Delivery Performance | 5000  | 8       |delivery_partner_id | order_id     |Delivery   | ✅         |
| Customer Feedback    | 5000  | 8       | feedback_id |order_id,customer_id | Customer  | ✅         |
| Marketing            | 5400  | 11      | campaign_id | -                   | Marketing | 🔄 Future  |

### Relationship Mapping

|`Primary Table`|`Related Table`      |`Join Column`|`Relationship`    |`Business Meaning`                          |
| ------------ | -------------------- | ----------- | ---------------- | ----------------------------------------- |
| Customers    | Orders               | customer_id | 1 : M            | One customer can place multiple orders.   |
| Orders       | Delivery Performance | order_id    | 1 : 1            | One order has one delivery record.        |
| Orders       | Customer Feedback    | order_id    | 1 : 1 (Optional) | Customers may or may not submit feedback. |
| Products     | Inventory            | product_id  | 1 : 1            | Each product has one inventory record.    |



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
|Transaction           | 50,000| 6        | transaction_id| order_id,product_id |Inventory & Sales| ✅     |

### Relationship Mapping

|`Primary Table`|`Related Table`|`Join Column`| `Relationship`|` Business Meaning`                          |
| ------------ | ----------- | ----------- | ---------------- | ----------------------------------------------- |
| Customers    | Orders      | customer_id | 1 : M            | One customer can place many orders.             |
| Orders       | Delivery    | order_id    | 1 : 1 (Optional) | Cancelled orders may not have delivery records. |
| Orders       | Rating      | order_id    | 1 : 1 (Optional) | Not every customer gives a rating.              |
| Orders       | Transaction | order_id    | 1 : M            | One order can contain multiple products.        |
| Products     | Transaction | product_id  | 1 : M            | One product can appear in many orders.          |


### Key Observations

- Date columns are stored as string.
- Primary and foreign keys identified.
- order_id are not same in other table (`delivery , rating , transcation`), 5000,7000 are not exist .
- missing 5000 order_id in rating table and transaction table are same .

### Cleaning Notes

- Convert date columns to `datetime`
- Validate primary key uniqueness
- Standardize column names and data value


##  Swiggy Instamart

| `Table`              | `Rows`| `Columns`| `PK `             | `FK`                | `Domain`    |`Decision`   |
| -------------------- | ----- | -------  | ---------------   | -------------------  | ---------  | ---------   |
| Orders               | 841   | 14       | order_id          | customerID,ProductID,StoreID,DeliveryPartner,PaymentMethodID
Delivery    | ✅    |
| Customers            | 50    | 7        | customerID        | AddressID           | Customer    | ✅         |
| Products             | 150   | 6        | product_id        | CategoryID,SupplierID | Inventory | ✅         |
| Categories           | 25    | 3        | CategoryID        | -                   |Inventory    | ✅         |
| Delivery_partner     | 50    | 5        | DeliveryPartnerID | AddressID           |delivery     | ✅         |
| Address              | 200   | 5        | AddressID         | -                   | Delivery    | ✅         |
| store                | 25    | 3        | StoreID           | AddressID           | Inventory   | ✅         |
| Payment Method       | 6     | 2        |  PaymentMethodID  | -                   | Delivery    | ✅         |

### Relationship Mapping

| `Primary Table`  | `Related Table`  |`Join Column`      |`Relationship`| `Business Meaning`                         |
| ---------------- | ---------------- | ----------------- | ------------ | ------------------------------------------ |
| Customers        | Orders           | customerID        | 1 : M        | Customers can place multiple orders.       |
| Categories       | Products         | categoryID        | 1 : M        | One category contains many products.       |
| Stores           | Orders           | storeID           | 1 : M        | One store fulfills many orders.            |
| Delivery Partner | Orders           | deliveryPartnerID | 1 : M        | One rider delivers many orders.            |
| Payment Method   | Orders           | paymentMethodID   | 1 : M        | One payment method is used by many orders. |
| Address          | Customers        | addressID         | 1 : M        | Multiple customers can share an address.   |
| Address          | Stores           | addressID         | 1 : 1        | One store has one address.                 |
| Address          | Delivery Partner | addressID         | 1 : 1        | One delivery partner has one address.      |


### Key Observations

- Date columns are stored as string.
- DeliveryTimeMinutes as int64.
- Primary and foreign keys identified.
- Payment methods table should be remove less data . paymentmethodID convert into payment mode where paymentmethodID exist.


## BigBasket and Jiomart

A dedicated BigBasket , Jiomart operational dataset containing normalized relational tables (Orders, Customers, Products, Inventory, etc.) was not publicly available.
To ensure consistent cross-platform comparison, the Quick Commerce Dataset was filtered using:

- Platform = BigBasket , Jiomart 
- City = Bengaluru

This produced a platform-specific dataset suitable for comparative analysis across delivery performance, customer feedback, and operational KPIs.

| `Table`          | `Rows` | `Columns` | `PK`       | `Domain`            |` Decision` |
| ---------------- | ----   | -------   | --------   | ------------------- | --------   |
| BigBasket_Orders | 9706   | 13        | order_id   | Delivery & Customer | ✅ Keep    |
| Jiomart          | 9805   | 13        | order_id   | delivery & customer | ✅ Keep    |


### Relationship Mapping

Not Applicable

Reason:
The datasets are already denormalized and contain a single table. Therefore, no inter-table relationships exist.

### Key Observations
- Dataset is already denormalized (single flat table).
- No separate Customer, Product or Inventory tables exist.
- Platform-specific filtering performed before analysis.
- Suitable for delivery and customer behavior analysis.
- Limited inventory analysis due to lack of product master and warehouse information.

