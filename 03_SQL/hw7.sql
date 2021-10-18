-- 1 --------------------------------------------------------
/*
 * 
 * 
 *  Составьте список пользователей users, 
 *  которые осуществили хотя бы один заказ orders 
 *  в интернет магазине.
 * 
 */

INSERT INTO shop.orders (user_id) 
  VALUES
    (2 ), (4);
 
INSERT INTO shop.orders_products (order_id, product_id, total) 
  VALUES
    (1, 2, 1), (1, 6, 1), (2, 1, 1), (3, 1, 10);
 
SELECT id FROM users WHERE id IN (SELECT user_id FROM orders);

-- 2 --------------------------------------------------------
/*
 * 
 *  Выведите список товаров products и разделов catalogs, 
 *  который соответствует товару.
 * 
 */

SELECT a.name AS product, b.name AS catalog_chapter 
 FROM products AS a 
 JOIN catalogs AS b 
 ON a.catalog_id = b.id;

-- 3* --------------------------------------------------------

/*
 * 
 *  (по желанию) Пусть имеется таблица рейсов flights (id, from, to) и 
 *  таблица городов cities (label, name). Поля from, to и label содержат 
 *  английские названия городов, поле name — русское. 
 *  Выведите список рейсов flights с русскими названиями городов.
 * 
 * 
 */

DROP TABLE IF EXISTS flights;
CREATE TABLE flights (
	id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
	`from` VARCHAR(200),
	`to` VARCHAR(200)
);

INSERT INTO flights (`from`, `to`) 
  VALUES
    ('moscow', 'omsk'),
    ('novgorod', 'kazan'),
    ('irkutsk', 'moscow'),
    ('omsk', 'irkutsk'),
    ('moscow', 'kazan');

DROP TABLE IF EXISTS cities;
CREATE TABLE cities(
  label VARCHAR(200),
  name VARCHAR(400)
)

INSERT INTO cities(label, name)
  VALUES
    ('moscow', 'Москва'),
    ('irkutsk', 'Иркутск'),
    ('novgorod', 'Новгород'),
    ('kazan', 'Казань'),
    ('omsk', 'Омск');
   
SELECT * FROM flights;

SELECT  a.id AS flight, CC.name AS `from` , CCC.name AS `to`
  FROM flights AS a 
  INNER JOIN cities AS CC ON a.`from` = CC.label 
  INNER JOIN cities  AS CCC ON a.`to` = CCC.label 
    ORDER BY a.id ;

 
 





