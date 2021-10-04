USE vk;

-- 1 --------------------------------------------------------
/*
 * 
 * Пусть в таблице users поля created_at и updated_at оказались незаполненными. Заполните их текущими датой и временем.
 * 
 */

ALTER TABLE vk.users DROP created_at;
ALTER TABLE vk.users ADD created_at DATETIME default NOW();
SELECT created_at FROM users;

ALTER TABLE vk.users DROP updated_at;
ALTER TABLE vk.users ADD updated_at DATETIME default NOW();
SELECT updated_at FROM users;

-- 2 --------------------------------------------------------
/*
 * 
 * Таблица users была неудачно спроектирована. Записи created_at и updated_at были заданы типом VARCHAR 
 * и в них долгое время помещались значения в формате "20.10.2017 8:10". 
 * Необходимо преобразовать поля к типу DATETIME, сохранив введеные ранее значения.
 * 
 */

ALTER TABLE vk.users DROP created_at;
ALTER TABLE vk.users ADD created_at VARCHAR(40);
ALTER TABLE vk.users DROP updated_at;
ALTER TABLE vk.users ADD updated_at VARCHAR(40);

SELECT firstname, lastname, phone FROM vk.users LIMIT 17;
INSERT INTO vk.users(firstname, lastname, phone, created_at, updated_at) 
VALUES  ('Abraham', 'Linkoln', 79168450120, '2020-07-01 17:47:33', '2021-01-06 17:47:33'),
		('Abraham', 'Linkoln 1', 79168450701, '2021-07-02 17:47:33', '2021-09-06 17:47:33'),
		('Abraham', 'Linkoln 2', 79168450602, '2021-07-03 17:47:33', '2021-10-06 17:47:33'),
		('Abraham', 'Linkoln 3', 79168450703, '2021-07-04 17:47:33', '2021-08-06 17:47:33'),
		('Abraham', 'Linkoln 4', 79168450704, '2021-07-05 17:47:33', '2021-12-06 17:47:33');
DELETE FROM users WHERE firstname = 'Abraham';
SELECT firstname, lastname, phone, created_at, updated_at FROM users WHERE firstname = 'Abraham';
DESC users;

ALTER TABLE vk.users MODIFY updated_at DATETIME;
ALTER TABLE vk.users MODIFY created_at DATETIME;
DESC users;   

SELECT VERSION() FROM DUAL;

-- 3 --------------------------------------------------------
/*
 * 
 * В таблице складских запасов storehouses_products в поле value 
 * могут встречаться самые разные цифры: 0, если товар закончился и выше нуля, 
 * если на складе имеются запасы. Необходимо отсортировать записи таким образом, 
 * чтобы они выводились в порядке увеличения значения value. 
 * Однако, нулевые запасы должны выводиться в конце, после всех записей.

 * 
 * 
 */

DROP TABLE IF EXISTS storehouses_products;
CREATE TABLE storehouses_products (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(20),
	value BIGINT UNSIGNED NOT NULL
);

INSERT INTO vk.storehouses_products(name, value) VALUES
/*
 * 
 * for i in [f"('www', '{random.randint(0, 10)}')" for x in range(0, 20)]:
 *     print(i)
 * 
 */
	('товар7', '1'),
	('товар9', '3'),
	('товар8', '2'),
	('товар1', '9'),
	('товар1', '4'),
	('товар10', '10'),
	('товар1', '0'),
	('товар5', '4'),
	('товар9', '8'),
	('товар1', '10'),
	('товар1', '6'),
	('товар7', '0'),
	('товар10', '0'),
	('товар9', '0'),
	('товар6', '0'),
	('товар8', '5'),
	('товар2', '4'),
	('товар4', '3'),
	('товар1', '10'),
	('товар1', '0');

SELECT * FROM storehouses_products sp HAVING value != 0 ORDER BY value;
SELECT * from storehouses_products WHERE value = 0;



SELECT value FROM 
(SELECT value FROM storehouses_products sp HAVING value != 0 ORDER BY value) as tt
   UNION ALL
(SELECT value FROM storehouses_products pp WHERE value = 0 ); 



-- 4* --------------------------------------------------------
/*
 * 
 * (по желанию) Из таблицы users необходимо извлечь пользователей, 
 * родившихся в августе и мае. 
 * Месяцы заданы в виде списка английских названий ('may', 'august')
 * 
 * 
 */


SELECT user_id, birthday as birthday FROM profiles WHERE MONTHNAME(birthday) IN ('March', 'August');

-- 1 --------------------------------------------------------
/*
 * 
 * Подсчитайте средний возраст пользователей в таблице users
 * 
 */

SELECT ROUND( AVG( YEAR(CURDATE()) - YEAR(birthday) ) ) from profiles;

-- 2 --------------------------------------------------------
/*
 * 
 * Подсчитайте количество дней рождения, 
 * которые приходятся на каждый из дней недели. 
 * Следует учесть, что необходимы дни недели текущего года, а не года рождения.
 * 
 */

SELECT DAYNAME(birthday), COUNT(*) from profiles GROUP BY  DAYNAME(birthday);
-- SELECT  user_id, CONCAT(DAY(birthday), '.', MONTH (birthday) ) FROM profiles; -- DAY(), DAYNAME() 
-- SELECT DAYNAME(birthday), birthday, '2021-03-20', DAYNAME('2021-03-20') From profiles WHERE user_id = 1;
-- SELECT YEAR(CURDATE() )

-- 3* --------------------------------------------------------
/*
 * 
 * (по желанию) Подсчитайте произведение чисел в столбце таблицы
 * 
 * 
 */

CREATE TABLE vk.calc ( num INT);
INSERT INTO vk.calc VALUES 
(1), (2), (3), (4), (5);
SELECT EXP(SUM(ln(num))) from calc;



