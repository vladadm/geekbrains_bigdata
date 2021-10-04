-- 1 --------------------------------------------------------
/*
 * 
 * Пусть задан некоторый пользователь. Из всех пользователей соц. сети найдите человека, 
 * который больше всех общался с выбранным пользователем (написал ему сообщений).
 *
 * 
 */

SELECT from_user_id , COUNT(*) as messages_from_user_id_7 
   FROM messages 
   WHERE to_user_id = 7 GROUP BY from_user_id  ORDER BY messages_from_user_id_7 DESC LIMIT 1;


-- 2 --------------------------------------------------------
/*
 * 
 * Подсчитать общее количество лайков, которые получили пользователи младше 10 лет.
 * 
 * 
 */

SELECT COUNT(*) from likes where user_id in (select user_id from profiles WHERE (birthday + INTERVAL 10 YEAR) > NOW());

-- 3 --------------------------------------------------------
/*
 * 
 * Определить кто больше поставил лайков (всего): мужчины или женщины.
 * 
 * 
 */

UPDATE profiles SET gender = 'm' WHERE user_id % 2;
UPDATE profiles SET gender = 'f' WHERE gender != 'm' ;

INSERT INTO likes(user_id, media_id) VALUES (1, 2), (2, 2), (3, 2);

-- male
-- SELECT user_id as man FROM profiles where gender = 'male';
-- female
-- SELECT user_id FROM profiles p where gender = 'female';

-- SELECT 
-- (SELECT COUNT(*) FROM likes WHERE user_id IN (SELECT user_id as man FROM profiles where gender = 'm')) as male, 
-- (SELECT COUNT(*) FROM likes WHERE user_id IN (SELECT user_id as man FROM profiles where gender = 'f')) as female;

SELECT gender_likes FROM
(SELECT COUNT(*) as gender_likes FROM likes WHERE user_id IN (SELECT user_id as man FROM profiles where gender = 'm')) as tt
  UNION 
(SELECT COUNT(*) as gender_likes FROM likes WHERE user_id IN (SELECT user_id as man FROM profiles where gender = 'f')) 
 ORDER BY gender_likes  DESC LIMIT 1

