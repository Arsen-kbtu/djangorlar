-- Django Models to SQL Schema Conversion
-- Generated for DB Designer import

-- =====================================================
-- CATALOGS APP TABLES
-- =====================================================

-- Restaurant table
CREATE TABLE catalogs_restaurant (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL,
    phone_number VARCHAR(20) NOT NULL
);

-- Category table
CREATE TABLE catalogs_category (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL
);

-- Option table
CREATE TABLE catalogs_option (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT
);

-- MenuItem table
CREATE TABLE catalogs_menuitem (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    restaurant_id INTEGER NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    base_price DECIMAL(10,2) NOT NULL,
    is_available BOOLEAN DEFAULT 1,
    FOREIGN KEY (restaurant_id) REFERENCES catalogs_restaurant(id) ON DELETE CASCADE
);

-- ItemCategory through table
CREATE TABLE catalogs_itemcategory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    menu_item_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    position INTEGER NOT NULL,
    FOREIGN KEY (menu_item_id) REFERENCES catalogs_menuitem(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES catalogs_category(id) ON DELETE CASCADE,
    UNIQUE(menu_item_id, category_id)
);

-- =====================================================
-- COMMERCES APP TABLES
-- =====================================================

-- Django User table (referenced by Address and Order)
-- Note: This is Django's built-in User model
CREATE TABLE auth_user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(150) NOT NULL UNIQUE,
    first_name VARCHAR(150),
    last_name VARCHAR(150),
    email VARCHAR(254),
    is_staff BOOLEAN DEFAULT 0,
    is_active BOOLEAN DEFAULT 1,
    date_joined DATETIME NOT NULL,
    password VARCHAR(128) NOT NULL
);

-- Address table
CREATE TABLE commerces_address (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    street VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    zip_code VARCHAR(20) NOT NULL,
    country VARCHAR(100) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE
);

-- PromoCode table
CREATE TABLE commerces_promocode (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code VARCHAR(50) NOT NULL UNIQUE,
    discount_percentage DECIMAL(5,2) NOT NULL,
    valid_from DATETIME NOT NULL,
    valid_to DATETIME NOT NULL,
    active BOOLEAN DEFAULT 1
);

-- Order table
CREATE TABLE commerces_order (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    restaurant_id INTEGER NOT NULL,
    address_id INTEGER NOT NULL,
    status VARCHAR(20) DEFAULT 'new',
    subtotal DECIMAL(10,2) NOT NULL,
    discount_total DECIMAL(10,2) DEFAULT 0,
    total DECIMAL(10,2) NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE,
    FOREIGN KEY (restaurant_id) REFERENCES catalogs_restaurant(id) ON DELETE CASCADE,
    FOREIGN KEY (address_id) REFERENCES commerces_address(id) ON DELETE CASCADE
);

-- OrderItem table
CREATE TABLE commerces_orderitem (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    menu_item_id INTEGER NOT NULL,
    item_name VARCHAR(255) NOT NULL,
    item_price DECIMAL(10,2) NOT NULL,
    quantity INTEGER NOT NULL,
    line_total DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES commerces_order(id) ON DELETE CASCADE,
    FOREIGN KEY (menu_item_id) REFERENCES catalogs_menuitem(id) ON DELETE CASCADE
);

-- OrderItemOption table
CREATE TABLE commerces_orderitemoption (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_item_id INTEGER NOT NULL,
    option_name VARCHAR(100) NOT NULL,
    price_delta DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_item_id) REFERENCES commerces_orderitem(id) ON DELETE CASCADE
);

-- OrderPromo through table
CREATE TABLE commerces_orderpromo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    promo_code_id INTEGER NOT NULL,
    applied_amount DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES commerces_order(id) ON DELETE CASCADE,
    FOREIGN KEY (promo_code_id) REFERENCES commerces_promocode(id) ON DELETE CASCADE,
    UNIQUE(order_id, promo_code_id)
);

-- =====================================================
-- MISSING THROUGH TABLE FROM MODELS
-- =====================================================
-- Note: The ItemOption through table is missing in your models.py
-- Based on the comment in MenuItem model, it should exist:

CREATE TABLE catalogs_itemoption (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    menu_item_id INTEGER NOT NULL,
    option_id INTEGER NOT NULL,
    price_delta DECIMAL(10,2) NOT NULL,
    is_default BOOLEAN DEFAULT 0,
    FOREIGN KEY (menu_item_id) REFERENCES catalogs_menuitem(id) ON DELETE CASCADE,
    FOREIGN KEY (option_id) REFERENCES catalogs_option(id) ON DELETE CASCADE,
    UNIQUE(menu_item_id, option_id)
);

-- =====================================================
-- INDEXES FOR BETTER PERFORMANCE
-- =====================================================

-- Indexes on foreign keys
CREATE INDEX idx_menuitem_restaurant ON catalogs_menuitem(restaurant_id);
CREATE INDEX idx_itemcategory_menuitem ON catalogs_itemcategory(menu_item_id);
CREATE INDEX idx_itemcategory_category ON catalogs_itemcategory(category_id);
CREATE INDEX idx_itemoption_menuitem ON catalogs_itemoption(menu_item_id);
CREATE INDEX idx_itemoption_option ON catalogs_itemoption(option_id);

CREATE INDEX idx_address_user ON commerces_address(user_id);
CREATE INDEX idx_order_user ON commerces_order(user_id);
CREATE INDEX idx_order_restaurant ON commerces_order(restaurant_id);
CREATE INDEX idx_order_address ON commerces_order(address_id);
CREATE INDEX idx_orderitem_order ON commerces_orderitem(order_id);
CREATE INDEX idx_orderitem_menuitem ON commerces_orderitem(menu_item_id);
CREATE INDEX idx_orderitemoption_orderitem ON commerces_orderitemoption(order_item_id);
CREATE INDEX idx_orderpromo_order ON commerces_orderpromo(order_id);
CREATE INDEX idx_orderpromo_promocode ON commerces_orderpromo(promo_code_id);

-- Indexes on frequently queried columns
CREATE INDEX idx_order_status ON commerces_order(status);
CREATE INDEX idx_order_created_at ON commerces_order(created_at);
CREATE INDEX idx_promocode_code ON commerces_promocode(code);
CREATE INDEX idx_promocode_active ON commerces_promocode(active);