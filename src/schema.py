"""
Schema definitions for all analytical tables.
"""

# ==========================
# Orders Table Schema
# ==========================

ORDERS_FINAL_COLUMNS = [
    "platform",
    "order_id",
    "customer_id",
    "product_id",
    "store_id",
    "delivery_partner_id",
    "order_datetime",
    "promised_delivery_datetime",
    "actual_delivery_datetime",
    "quantity",
    "order_value",
    "discount_applied",
    "delivery_time_minutes",
    "order_status",
    "payment_method_id",
    "time_of_day",
]