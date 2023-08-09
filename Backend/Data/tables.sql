CREATE TABLE category (
    category_id VARCHAR PRIMARY KEY,
    category_name VARCHAR,
    parent_name VARCHAR
);

CREATE TABLE product (
    product_id VARCHAR PRIMARY KEY,
    name VARCHAR,
    price FLOAT,
    description VARCHAR,
    image_url VARCHAR,
    category_id VARCHAR,
    FOREIGN KEY (category_id) REFERENCES category (category_id)
);
