select count(*) from analitycs.orders;

-- Поиск нелинейностей
-- выбросы
select * 
  from analitycs.orders 
  order by price asc ;
 
select * 
  from analitycs.orders 
  order by price desc ;
 
-- дубли
select count(*), count(distinct(id_o))
  from analitycs.orders 
  order by price desc;
 
-- кол-во заказов по дням
select o_date, count(id_o) as order_count
  from analitycs.orders
  group by o_date order by order_count;
 
-- кол-во заказов на пользователя
select user_id, count(id_o)
  from analitycs.orders
  group by user_id 
    order by count(id_o) desc; 
 

-- 2 Определить период заказов
select (select distinct(orders.o_date) from analitycs.orders order by o_date limit 1) as first_date,
       (select distinct(orders.o_date) from analitycs.orders order by o_date desc limit 1) as last_date;

-- 3 Общее кол-во строк, общее кол-во уникальных заказов, общее кол-во пользователей
select (select count(*) from analitycs.orders) as total_rows,
       (select count(orders) from (select distinct(id_o) from analitycs.orders) as orders) as total_orders,
       (select count(users) from (select distinct(user_id) from analitycs.orders) as users) as total_users;

      
-- describe
-- select column_name, data_type from information_schema.columns where table_name = 'orders';

-- alter table analitycs.orders add column price_new float;
-- alter table analitycs.orders add column date_new date;

-- column type convert
-- alter table analitycs.orders alter COLUMN price TYPE float USING replace(price, ',','.')::float;
-- alter table analitycs.orders alter COLUMN o_date TYPE date USING to_date(o_date, 'DD-MM-YYYY')::date;

-- describe
-- select column_name, data_type from information_schema.columns where table_name = 'orders';


-- 4 средний чек по месяцам
select
	extract(year from o_date) as year,
	extract(month from o_date) as month,
	round(avg(price)::numeric, 2) as avg_price
from
	analitycs.orders
group by
	extract(year from o_date),
	extract(month from o_date);

select extract(month from o_date), avg(count ) from (select o_date, user_id, count(id_o)
  from analitycs.orders group by extract(month from o_date), user_id) as mm;

-- 6 покупатели которые покупали в 2016 и не покупали в 2017
select distinct(user_id) 
from analitycs.orders 
	where extract(year from o_date) = 2016 and  user_id not in 
	(select distinct(user_id)
	  from analitycs.orders o  where extract(year from o_date) = 2017);

-- 6 больше всех купивший

-- select user_id, count(id_o) as cc from analitycs.orders group by user_id order by cc desc limit 1;

select user_id, count(id_o)
from analitycs.orders 
  group by user_id 
having count(id_o) = (
  select max(users.total_orders)
    from (
    select count(id_o) as total_orders
      from analitycs.orders
    group by user_id
        ) users ) ;

-- 7 Коэффициент сезонности
select 
  extract(year from o_date),
  extract(month from o_date), 
  round(sum(price)::numeric, 2)
from analitycs.orders
  --where extract(year from o_date) = 2016
  group by extract(year from o_date), 
           extract(month from o_date);


