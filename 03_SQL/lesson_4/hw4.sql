-- 1 --------------------------------------------------------

USE vk;
ALTER TABLE vk.profiles ADD is_active BIT default 1;

-- 2 --------------------------------------------------------

SELECT COUNT(id) FROM users;
SELECT DISTINCT firstname FROM users ORDER BY firstname;
SELECT COUNT(DISTINCT firstname) FROM users ORDER BY firstname;

-- 3 --------------------------------------------------------

SELECT user_id, birthday, is_active FROM profiles p WHERE is_active = 0;
UPDATE profiles SET is_active = 0 WHERE (birthday + INTERVAL 18 YEAR) > NOW();
SELECT user_id, birthday, is_active FROM profiles p WHERE is_active = 0;

-- 4 --------------------------------------------------------

DELETE FROM messages WHERE created_at > NOW();

-- 5 --------------------------------------------------------

/* 
 *
 *  
	Тема курсового проекта:
	Модель данных описывающая туристические путевки 
	* страны
	* города
	* туры
	* авиабилеты
	* авиарейсы
	* авиакомпании
	* аэропорты
	* гостиницы
	* ...
 *
 *
 *
*/