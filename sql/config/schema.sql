-- Lendo o arquivo orders.csv
CREATE TABLE IF NOT EXISTS orders (
    "id" INTEGER,
    "order_number" TEXT,
    "channel" TEXT,
    "customer_id" INTEGER,
    "location_id" INTEGER,
    "status" TEXT,
    "subtotal" DOUBLE PRECISION,
    "discount_amount" DOUBLE PRECISION,
    "total" DOUBLE PRECISION,
    "placed_at" DATETIME,
    "created_at" DATETIME,
    "updated_at" DATETIME,
    "salesperson_id" INTEGER
);

-- Lendo o arquivo variant_attribute_values.csv
CREATE TABLE IF NOT EXISTS variant_attribute_values (
    "product_variant_id" INTEGER,
    "attribute_id" INTEGER,
    "value" TEXT
);

-- Lendo o arquivo purchase_orders.csv
CREATE TABLE IF NOT EXISTS purchase_orders (
    "id" INTEGER,
    "po_number" TEXT,
    "supplier_id" INTEGER,
    "buyer_id" INTEGER,
    "destination_location_id" INTEGER,
    "status" TEXT,
    "currency" TEXT,
    "subtotal" DOUBLE PRECISION,
    "total" DOUBLE PRECISION,
    "placed_at" DATETIME,
    "expected_delivery_at" DATE,
    "created_at" DATETIME,
    "updated_at" DATETIME
);

-- Lendo o arquivo suppliers.csv
CREATE TABLE IF NOT EXISTS suppliers (
    "id" INTEGER,
    "legal_name" TEXT,
    "trade_name" TEXT,
    "country" TEXT,
    "tax_id" INTEGER,
    "tax_id_type" TEXT,
    "email" TEXT,
    "phone" TEXT,
    "contact_name" TEXT,
    "is_active" BOOLEAN,
    "created_at" DATETIME,
    "updated_at" DATETIME
);

-- Lendo o arquivo returns.csv
CREATE TABLE IF NOT EXISTS returns (
    "id" INTEGER,
    "return_number" TEXT,
    "order_id" INTEGER,
    "customer_id" INTEGER,
    "received_at_location_id" INTEGER,
    "status" TEXT,
    "reason" TEXT,
    "total_refund_amount" DOUBLE PRECISION,
    "created_at" DATETIME,
    "updated_at" DATETIME
);

-- Lendo o arquivo stock_movements.csv
CREATE TABLE IF NOT EXISTS stock_movements (
    "id" INTEGER,
    "product_variant_id" INTEGER,
    "location_id" INTEGER,
    "movement_type" TEXT,
    "quantity" DOUBLE PRECISION,
    "notes" TEXT,
    "occurred_at" DATETIME,
    "created_at" DATETIME
);

-- Lendo o arquivo customers.csv
CREATE TABLE IF NOT EXISTS customers (
    "id" INTEGER,
    "person_type" TEXT,
    "legal_name" TEXT,
    "trade_name" TEXT,
    "tax_id" INTEGER,
    "state_registration" TEXT,
    "email" TEXT,
    "phone" TEXT,
    "is_active" BOOLEAN,
    "created_at" DATETIME,
    "updated_at" DATETIME
);

-- Lendo o arquivo employees.csv
CREATE TABLE IF NOT EXISTS employees (
    "id" INTEGER,
    "full_name" TEXT,
    "cpf" TEXT,
    "email" TEXT,
    "role" TEXT,
    "primary_location_id" INTEGER,
    "hire_date" DATE,
    "is_active" BOOLEAN,
    "created_at" DATETIME,
    "updated_at" DATETIME
);

-- Lendo o arquivo categories.csv
CREATE TABLE IF NOT EXISTS categories (
    "id" INTEGER,
    "name" TEXT,
    "slug" TEXT,
    "is_active" BOOLEAN,
    "created_at" DATETIME,
    "updated_at" DATETIME
);

-- Lendo o arquivo stock_levels.csv
CREATE TABLE IF NOT EXISTS stock_levels (
    "product_variant_id" INTEGER,
    "location_id" INTEGER,
    "quantity_on_hand" DOUBLE PRECISION,
    "updated_at" DATETIME
);

-- Lendo o arquivo products.csv
CREATE TABLE IF NOT EXISTS products (
    "id" INTEGER,
    "name" TEXT,
    "description" TEXT,
    "brand_id" INTEGER,
    "category_id" INTEGER,
    "ncm_code" INTEGER,
    "unit_of_measure" TEXT,
    "is_active" BOOLEAN,
    "created_at" DATETIME,
    "updated_at" DATETIME
);

-- Lendo o arquivo purchase_order_items.csv
CREATE TABLE IF NOT EXISTS purchase_order_items (
    "id" INTEGER,
    "purchase_order_id" INTEGER,
    "product_variant_id" INTEGER,
    "quantity_ordered" INTEGER,
    "unit_cost" DOUBLE PRECISION,
    "line_total" DOUBLE PRECISION
);

-- Lendo o arquivo goods_receipt_items.csv
CREATE TABLE IF NOT EXISTS goods_receipt_items (
    "id" INTEGER,
    "goods_receipt_id" INTEGER,
    "purchase_order_item_id" INTEGER,
    "quantity_received" DOUBLE PRECISION
);

-- Lendo o arquivo attributes.csv
CREATE TABLE IF NOT EXISTS attributes (
    "id" INTEGER,
    "name" TEXT,
    "data_type" TEXT
);

-- Lendo o arquivo locations.csv
CREATE TABLE IF NOT EXISTS locations (
    "id" INTEGER,
    "name" TEXT,
    "location_type" TEXT,
    "postal_code" TEXT,
    "street" TEXT,
    "number" INTEGER,
    "complement" TEXT,
    "district" TEXT,
    "city" TEXT,
    "state" TEXT,
    "country" TEXT,
    "is_active" BOOLEAN,
    "created_at" DATETIME,
    "updated_at" DATETIME
);

-- Lendo o arquivo fiscal_invoices.csv
CREATE TABLE IF NOT EXISTS fiscal_invoices (
    "id" INTEGER,
    "order_id" INTEGER,
    "nfe_number" TEXT,
    "nfe_access_key" INTEGER,
    "series" INTEGER,
    "issued_at" DATETIME,
    "status" TEXT,
    "total_amount" DOUBLE PRECISION,
    "xml_storage_uri" TEXT,
    "created_at" DATETIME,
    "updated_at" DATETIME
);

-- Lendo o arquivo payments.csv
CREATE TABLE IF NOT EXISTS payments (
    "id" INTEGER,
    "order_id" INTEGER,
    "method" TEXT,
    "installments" INTEGER,
    "amount" DOUBLE PRECISION,
    "status" TEXT,
    "paid_at" DATETIME,
    "created_at" DATETIME,
    "updated_at" DATETIME
);

-- Lendo o arquivo goods_receipts.csv
CREATE TABLE IF NOT EXISTS goods_receipts (
    "id" INTEGER,
    "purchase_order_id" INTEGER,
    "received_by_employee_id" INTEGER,
    "received_at" DATETIME,
    "created_at" DATETIME
);

-- Lendo o arquivo return_items.csv
CREATE TABLE IF NOT EXISTS return_items (
    "id" INTEGER,
    "return_id" INTEGER,
    "order_item_id" INTEGER,
    "quantity" DOUBLE PRECISION,
    "action" TEXT,
    "unit_refund_amount" DOUBLE PRECISION
);

-- Lendo o arquivo product_suppliers.csv
CREATE TABLE IF NOT EXISTS product_suppliers (
    "product_variant_id" INTEGER,
    "supplier_id" INTEGER,
    "supplier_sku" TEXT,
    "last_quoted_cost" DOUBLE PRECISION,
    "lead_time_days" INTEGER,
    "is_preferred" BOOLEAN,
    "created_at" DATETIME,
    "updated_at" DATETIME
);

-- Lendo o arquivo product_variants.csv
CREATE TABLE IF NOT EXISTS product_variants (
    "id" INTEGER,
    "product_id" INTEGER,
    "sku" TEXT,
    "barcode_ean" INTEGER,
    "sale_price" DOUBLE PRECISION,
    "cost_price" DOUBLE PRECISION,
    "weight_kg" DOUBLE PRECISION,
    "icms_rate" DOUBLE PRECISION,
    "ipi_rate" DOUBLE PRECISION,
    "is_active" BOOLEAN,
    "created_at" DATETIME,
    "updated_at" DATETIME
);

-- Lendo o arquivo brands.csv
CREATE TABLE IF NOT EXISTS brands (
    "id" INTEGER,
    "name" TEXT,
    "is_active" BOOLEAN,
    "created_at" DATETIME,
    "updated_at" DATETIME,
    "country" TEXT
);

-- Lendo o arquivo addresses.csv
CREATE TABLE IF NOT EXISTS addresses (
    "id" INTEGER,
    "customer_id" INTEGER,
    "address_type" TEXT,
    "postal_code" TEXT,
    "street" TEXT,
    "number" INTEGER,
    "district" TEXT,
    "city" TEXT,
    "state" TEXT,
    "country" TEXT,
    "is_primary" BOOLEAN
);

-- Lendo o arquivo order_items.csv
CREATE TABLE IF NOT EXISTS order_items (
    "id" INTEGER,
    "order_id" INTEGER,
    "product_variant_id" INTEGER,
    "quantity" INTEGER,
    "unit_price" DOUBLE PRECISION,
    "icms_rate" DOUBLE PRECISION,
    "ipi_rate" DOUBLE PRECISION,
    "line_total" DOUBLE PRECISION
);

