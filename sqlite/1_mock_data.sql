INSERT INTO statuses (id, name, slug) VALUES
(1, 'Nou', 'nou');
UPDATE SQLITE_SEQUENCE SET seq = 1 WHERE name = 'statuses';

INSERT INTO categories (id, name, slug) VALUES
(1, 'Electrònica', 'electronica'),
(2, 'Roba', 'roba'),
(3, 'Joguines', 'joguines');
UPDATE SQLITE_SEQUENCE SET seq = 3 WHERE name = 'categories';

-- Les contrasenyes són patata
INSERT INTO users (id, name, email, role, verified, password) VALUES
(1, 'Joan Pérez', 'joan@example.com', 'admin', TRUE, 'scrypt:32768:8:1$lwqNpblQ9OiKBfeM$4d63ebdf494cc8e363f14494bca1c5246f6689b45904431f69fbcb535b7e41bd012e9b41c850125d7f8b790cb320579a46427b69eda892517669eba0244b77b4'),
(2, 'Anna García', 'anna@example.com', 'moderator', TRUE, 'scrypt:32768:8:1$lwqNpblQ9OiKBfeM$4d63ebdf494cc8e363f14494bca1c5246f6689b45904431f69fbcb535b7e41bd012e9b41c850125d7f8b790cb320579a46427b69eda892517669eba0244b77b4'),
(3, 'Elia Rodríguez', 'elia@example.com', 'wanner', TRUE, 'scrypt:32768:8:1$lwqNpblQ9OiKBfeM$4d63ebdf494cc8e363f14494bca1c5246f6689b45904431f69fbcb535b7e41bd012e9b41c850125d7f8b790cb320579a46427b69eda892517669eba0244b77b4'),
(4, 'Kevin Salardú', 'kevin@example.com', 'wanner', TRUE, 'scrypt:32768:8:1$lwqNpblQ9OiKBfeM$4d63ebdf494cc8e363f14494bca1c5246f6689b45904431f69fbcb535b7e41bd012e9b41c850125d7f8b790cb320579a46427b69eda892517669eba0244b77b4');
UPDATE SQLITE_SEQUENCE SET seq = 4 WHERE name = 'users';

-- Inserir dades fictícies a la taula products
INSERT INTO products (id, title, description, photo, price, category_id, status_id, seller_id) VALUES
(1, 'Telèfon mòbil', 'Un telèfon intel·ligent d''última generació.', 'no_image.png', 599.99, 1, 1, 3),
(2, 'Samarreta', 'Una samarreta de cotó de color blau.', 'no_image.png', 19.99, 2, 1, 3),
(3, 'Ninot de peluix', 'Un ninot de peluix suau.', 'no_image.png', 9.99, 3, 1, 4);
UPDATE SQLITE_SEQUENCE SET seq = 3 WHERE name = 'products';

-- Inserir dades a la taula stores
INSERT INTO stores(id, nom) VALUES (1, "Mercadona");
INSERT INTO stores(id, nom) VALUES (2, "Lidl");
INSERT INTO stores(id, nom) VALUES (3, "Aldi");
INSERT INTO stores(id, nom) VALUES (4, "Condis");
UPDATE SQLITE_SEQUENCE SET seq = 4 WHERE name = 'stores';

--Inserir dades a la taula items
INSERT INTO items(id, store_id, nom, unitats) VALUES (1,1,"Bike",888);
INSERT INTO items(id, store_id, nom, unitats) VALUES (2,1,"Skate",296);
INSERT INTO items(id, store_id, nom, unitats) VALUES (3,1,"Surfskate",343);
INSERT INTO items(id, store_id, nom, unitats) VALUES (4,2,"Banana",15);
INSERT INTO items(id, store_id, nom, unitats) VALUES (5,2,"Orange",168);
INSERT INTO items(id, store_id, nom, unitats) VALUES (6,2,"Apple",214);
INSERT INTO items(id, store_id, nom, unitats) VALUES (7,3,"Bacon",589);
INSERT INTO items(id, store_id, nom, unitats) VALUES (8,3,"Chicken",250);
INSERT INTO items(id, store_id, nom, unitats) VALUES (9,3,"Sausage",538);
UPDATE SQLITE_SEQUENCE SET seq = 9 WHERE name = 'items';

--Inserir dades a la taula discounts
INSERT INTO discounts(item_id,discount) VALUES (1,10);
INSERT INTO discounts(item_id,discount) VALUES (3,20);
INSERT INTO discounts(item_id,discount) VALUES (5,30);
INSERT INTO discounts(item_id,discount) VALUES (7,40);
INSERT INTO discounts(item_id,discount) VALUES (9,50);

-- Inserción en la tabla orders
INSERT INTO orders (product_id, buyer_id, offer, created) VALUES
(1, 1, 499.99, DATETIME('now')),
(2, 2, 15.99, DATETIME('now')),
(3, 3, 7.99, DATETIME('now'));

-- Inserción en la tabla confirmed_orders
INSERT INTO confirmed_orders (order_id, created) VALUES
(1, DATETIME('now')),
(2, DATETIME('now')),
(3, DATETIME('now'));