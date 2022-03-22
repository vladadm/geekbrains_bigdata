/* Задание 1 */

-- Удаляем базу student42_19 если она существует
drop database if exists student42_19 cascade;

-- Выводим список доуступных баз данных
show databases;
-- Выводим список доступных таблиц всех баз данных
show tables;

-- Создаем базу student42_19 если она не существует
create database if not exists student42_19;

--зачем используем use?
-- переключаемся на базу student42_19
use student42_19;
-- Выводим список таблиц student42_19
show tables;

-- Удаляем таблицы если они существуют ( student42_1 указывать не обязательно т.к. выше мы выполнили use student42_19 )
drop table if exists student42_19.airport_codes;
drop table if exists student42_19.airport_codes_part;

--"id","ident","type","name","latitude_deg","longitude_deg","elevation_ft","continent","iso_country","iso_region","municipality","scheduled_service","gps_code","iata_code","local_code","home_link","wikipedia_link","keywords"
--6523,"00A","heliport","Total Rf Heliport",40.07080078125,-74.93360137939453,11,"NA","US","US-PA","Bensalem","no","00A",,"00A",,,
--323361,"00AA","small_airport","Aero B Ranch Airport",38.704022,-101.473911,3435,"NA","US","US-KS","Leoti","no","00AA",,"00AA",,,
--6524,"00AK","small_airport","Lowell Field",59.947733,-151.692524,450,"NA","US","US-AK","Anchor Point","no","00AK",,"00AK",,,
--6525,"00AL","small_airport","Epps Airpark",34.86479949951172,-86.77030181884766,820,"NA","US","US-AL","Harvest","no","00AL",,"00AL",,,

-- Создаем внешнюю таблицу airport_codes
create external table airport_codes (
    id int,
    ident string,
    `type` string,
    name string,
    latitude_deg string,
    longitude_deg string,
    elevation_ft string,
    continent string,
    iso_country string,
    iso_region string,
    municipality string,
    scheduled_service string,
    gps_code string, 
    iata_code string,
    local_code string,
    home_link string,
    wikipedia_link string,
    keywords string
)
row format delimited fields terminated by ',' --ESCAPED BY '"' -- разделитель
stored as textfile
location "/user/student42_1/airports" -- папка на hdfs в которой будут храниться файлы с данными этой таблици
tblproperties ("skip.header.line.count"="1") --зачем нам эта опция? -- при импорте данных из файла в эту таблицу первая строка будет игнорироваться
;
-- выводим метаинформацию (DDL) по созданной таблице
show create table airport_codes
;

-- удалем таблицу 
drop table airport_codes;

select * from airport_codes limit 10; --почему пишем лимит? -- для вывода первых 10 строк из выборки

--что делаем в этих запросах?
select count(distinct `type`) from airport_codes; -- выводим кол-во уникальных значений колонки TYPE из таблици airport_codes
select distinct `type` from airport_codes; -- выводим уникальные значения колонки TYPE из таблици airport_codes

-- удаляем таблицу student42_19.airport_codes_part если она существует
drop table if exists student42_19.airport_codes_part;

-- создаем таблицу airport_codes_part и выносим поле type в отдельную партицию
create table airport_codes_part (
    id int,
    ident string,
    name string,
    latitude_deg string,
    longitude_deg string,
    elevation_ft string,
    continent string,
    iso_country string,
    iso_region string,
    municipality string,
    scheduled_service string,
    gps_code string, 
    iata_code string,
    local_code string,
    home_link string,
    wikipedia_link string,
    keywords string
)
partitioned by (`type` string)
row format delimited fields terminated by ','
stored as textfile
location '/user/student42_19/airport_codes_part'
;

show tables;

-- выводим метаинформацию (DDL) по таблице
show create table airport_codes_part;

-- Устанавливаем настройку hive для возможности создавать новые партиции
set hive.exec.dynamic.partition.mode=nonstrict;

-- выбираем данные из всех колонок таблицы airport_codes_part и выводим первые 10 строк
select * from airport_codes_part limit 10;

-- вставляем 1000 строк в таблицу airport_codes_part с партицией по полю type выборкой из внешней таблицы airport_codes
insert into table airport_codes_part 
partition(`type`)
select
    id,ident,name,latitude_deg,longitude_deg,elevation_ft,
    continent,iso_country,iso_region,municipality,scheduled_service,
    gps_code,iata_code,local_code,home_link,wikipedia_link,keywords,
    `type`
from airport_codes
tablesample (1000 rows); -- выбираем случаным образом 1000 строк

-- выбираем данные из всех полей таблицы airport_codes_part и выводим первые 10 строк
select * from airport_codes_part /*tablesample (10 rows)*/ limit 10;

-- выводим кол-во уникальных значений поля TYPE из таблици airport_codes_part§
select count(distinct `type`) as t from airport_codes_part;

-- выводим уникальные значения поля TYPE из таблици airport_codes_part
select distinct `type` from airport_codes_part;

-- из таблицы airport_codes_part , группируем по полю `type` и сортируем в порядке убывания и выводим значение +  кол-во значений
select 
	`type`, count(1)
from airport_codes_part
group by `type`
order by 2 desc;

/*
[student42_19@bigdataanalytics-worker-3 ~]$ hdfs dfs -ls airport_codes_part
Found 4 items
drwxr-xr-x   - student42_19 student42_19          0 2022-02-10 15:24 airport_codes_part/type=%22closed%22
drwxr-xr-x   - student42_19 student42_19          0 2022-02-10 15:24 airport_codes_part/type=%22heliport%22
drwxr-xr-x   - student42_19 student42_19          0 2022-02-10 15:24 airport_codes_part/type=%22seaplane_base%22
drwxr-xr-x   - student42_19 student42_19          0 2022-02-10 15:24 airport_codes_part/type=%22small_airport%22

-- добавляем новую партицию непосредственно на hdfs
-- hdfs dfs -cp /user/student42_19/airport_codes_part/type=%22small_airport%22 /user/student42_19/airport_codes_part/type=new_type

[student42_19@bigdataanalytics-worker-3 ~]$ hdfs dfs -ls airport_codes_part
Found 5 items
drwxr-xr-x   - student42_19 student42_19          0 2022-02-10 15:24 airport_codes_part/type=%22closed%22
drwxr-xr-x   - student42_19 student42_19          0 2022-02-10 15:24 airport_codes_part/type=%22heliport%22
drwxr-xr-x   - student42_19 student42_19          0 2022-02-10 15:24 airport_codes_part/type=%22seaplane_base%22
drwxr-xr-x   - student42_19 student42_19          0 2022-02-10 15:24 airport_codes_part/type=%22small_airport%22
drwxr-xr-x   - student42_19 student42_19          0 2022-02-10 15:27 airport_codes_part/type=new_type

*/

-- восстанавливаем таблицу после добавления новой партиции непосредственно на hdfs 
msck repair table airport_codes_part;

-- видим что партицию добавлися новый тип new_type
select distinct `type` from airport_codes_part;

/*
"closed"
"heliport"
new_type
"seaplane_base"
"small_airport"
 */

-- удаляем партицию из поля type со значением new_type ( так лучше не делать )
ALTER TABLE airport_codes_part DROP IF EXISTS PARTITION(`type`='new_type');

-- видим что из партиции удалился тип new_type
select distinct `type` from airport_codes_part;

/*
"closed"
"heliport"
"seaplane_base"
"small_airport"
 */

-- если удаляем тип из партиции на hdfs таже нужно выполнять:
MSCK REPAIR TABLE airport_codes_part;

/*
теперь посмотри в path через hdfs dfs -ls/-du и скажи, что заметил и почему там всё так
*/
-- c hdfs удалился файл airport_codes_part/type=new_type

-- удаляем таблицу for_insert_airport_codes_part
drop table for_insert_airport_codes_part;

--что такое temporary table и когда лучше использовать? 
-- временная таблица ( храниться во временной директории tmp ), действет в рамках сесии ( как только сессия прерывается таблица удаляеться )
-- может использоваться для оптимизации запросов, создаеться на основе данных из выборки или подгружаемых данных из файла 

--что будет с содержимым таблицы, если колонки, по которым партиционируем, будут стоять не последними в селекте?
-- hive создаст новые партиции на hdfs

-- создаем временную таблицу и наполняе её данными выборки из запроса 
create temporary table for_insert_airport_codes_part as
select 
     t1.*
from student42_1.airport_codes t1
left join (
    select distinct
        `type` as type_2
    from student42_19.airport_codes_part
    ) t2 on t1.`type` = t2.type_2
where 
    t2.type_2 is null
;

-- выводим выборку всех данных по всем полям из временной таблицы for_insert_airport_codes_part
select * from for_insert_airport_codes_part;

select count(distinct `type`) from for_insert_airport_codes_part;

select distinct `type` from for_insert_airport_codes_part;


--чем insert overwrite отличается от insert into?
insert into student42_19.airport_codes_part partition(`type`)
select 
     id,ident,name,latitude_deg,longitude_deg,elevation_ft,
     continent,iso_country,iso_region,municipality,scheduled_service,
     gps_code,iata_code,local_code,home_link,wikipedia_link,keywords,`type`
from for_insert_airport_codes_part t1
limit 1;

/*
select count(id) from airport_codes_part;
insert overwrite table student42_19.airport_codes_part partition(`type`)
select 
     id,ident,name,latitude_deg,longitude_deg,elevation_ft,
     continent,iso_country,iso_region,municipality,scheduled_service,
     gps_code,iata_code,local_code,home_link,wikipedia_link,keywords,`type`
from for_insert_airport_codes_part t1
limit 1;
select * from airport_codes_part limit 1;
*/

-- при insert owerwrite происходит удаление всех аналогичных строк и запись новой

select count(distinct `type`) from airport_codes_part;
select * from airport_codes_part limit 1;

select distinct `type` from airport_codes_part;

/*
STREAMING
выполни в баше это и скажи, что мы тут делаем:
    seq 0 9 > col_1 && seq 10 19 > col_2
    -- выполняем перебор от 0 до 9 и результат вывода записываем в файл col_1,
    выполняем перебор от 10 до 19 и результат вывода записываем в файл col_2
    paste -d'|' col_1 col_2 | hdfs dfs -appendToFile - test_tab/test_tab.csv
    -- объединеям содержимое двух файлов с разделителем | и вывод записываем на hdfs в файл test_tab/test_tab.csv
*/

--удаляем если существует таблицу my_test_tab
drop table if exists my_test_tab;

-- создаем временную таблицу, с данными из файла test_tab.cvs
create temporary external table my_test_tab (
    col_1 int,
    col_2 int
)
row format delimited fields terminated by '|' -- указываем разделитель |
stored as TEXTFILE  -- формат хранения 
location "/user/student42_19/test_tab" -- файл в который смотрит /user/student42_1/test_tab
;
select * from my_test_tab;

-- вставляем в таблицу новые значения
insert into table my_test_tab values (21, 31);

-- проверяем что они появились
select * from my_test_tab;

-- но в не повились в файле
/*
 [student42_19@bigdataanalytics-worker-3 ~]$ hdfs dfs -cat test_tab/test_tab.csv
0|10
1|11
2|12
3|13
4|14
5|15
6|16
7|17
8|18
9|19
 */


--что тут произошло и как это можно использовать ещё?
-- суммируем с помошью bash и awk значения полей, 
-- можно использовать для преобразования текстового потока с помощью скриптов написанных на любом языке
select
   transform(col_1, col_2) using "awk '{print $1+$2}'" as my_sum
from my_test_tab
;

-- /home/student42_1/mapred/mapper.py 

---------------------
/* Задание 2 
Сказать какие особенности, касающиеся синтаксиса HiveQL надо учитывать, 
создавая таблицу с партиционированием и при инсерте в неё. 
Зачем нам нужно партиционирование?
*/

/*
 Нужно обязательно указывать тип таблицы, при перечислении полей не указывать партицируемую,
 указывать разделитель полей, формат хранения, и папку в которой будут храниться данные на hdfs
 При инсерет в таблицу с партиционированием необходимо строго соблюдать последовательность полей ( смотреть show create table ), 
 инача червато тем, что hive создаст новые партиции на hdfs и таблица будет поломана.
 Партицирование служит для оптимизации скорости выполнения запросов, распределение хранения, и экономии места.
 
 */

--------------------
/* Задание 3 
 Переписать «select …» в команде «create temporary table» используя “with” для объявления t2
 */


create temporary table for_insert_my_statement as
WITH t1 as (SELECT `type` from airport_codes where `type` like '%closed%' limit 1), 
t2 as (SELECT ident from airport_codes where `type` = '"closed"' limit 1),
t3 as (SELECT iso_region from airport_codes where ident = '"00AL"' limit 1)
SELECT * from t1 
UNION ALL
SELECT * from t2
UNION ALL 
SELECT * from t3;

show create table for_insert_my_statement;

select * from for_insert_my_statement;

----------------------
/* Задание '*'
 
Создать таблицу airport_codes_part_2 c партиционированием по 2 колонкам: type и iso_country. 
Вставить в неё 1000 строк, запросом select вывести самую популярную связку type iso_country 
используя оконную функцию row_number https://www.revisitclass.com/hadoop/how-to-use-row-number-function-in-hive/
 
 */

drop table if exists airport_codes_part_2;

create table airport_codes_part_2 (
    id int,
    ident string,
    name string,
    latitude_deg string,
    longitude_deg string,
    elevation_ft string,
    continent string,
    iso_region string,
    municipality string,
    scheduled_service string,
    gps_code string, 
    iata_code string,
    local_code string,
    home_link string,
    wikipedia_link string,
    keywords string
)
partitioned  by (iso_country string, `type` string)
row format delimited fields terminated by ','
stored as textfile
location '/user/student42_19/airport_codes_part_2'
;

/*
[student42_19@bigdataanalytics-worker-3 ~]$ hdfs dfs -ls
Found 6 items
drwx------   - student42_19 student42_19          0 2022-02-10 15:30 .Trash
drwxr-xr-x   - student42_19 student42_19          0 2022-02-10 11:40 .hiveJars
drwxr-xr-x   - student42_19 student42_19          0 2022-02-10 16:30 airport_codes_part
drwxr-xr-x   - student42_19 student42_19          0 2022-02-10 17:14 airport_codes_part_2
-rw-r--r--   2 student42_19 student42_19          6 2022-02-01 17:51 test_file_1
drwxr-xr-x   - student42_19 student42_19          0 2022-02-10 15:52 test_tab

[student42_19@bigdataanalytics-worker-3 ~]$ hdfs dfs -ls airport_codes_part_2
[student42_19@bigdataanalytics-worker-3 ~]$
 */

show create table airport_codes_part_2;

set hive.exec.dynamic.partition.mode=nonstrict;

insert into table airport_codes_part_2
partition(iso_country, `type`)
select
    id,ident,name,latitude_deg,longitude_deg,elevation_ft,
    continent,iso_region,municipality,scheduled_service,
    gps_code,iata_code,local_code,home_link,wikipedia_link,keywords,
    iso_country, `type`
from airport_codes
tablesample (1000 rows);

explain select * from airport_codes_part_2 limit 10;

/*
[student42_19@bigdataanalytics-worker-3 ~]$ hdfs dfs -du airport_codes_part_2
152     304     airport_codes_part_2/iso_country=%22MH%22
266     532     airport_codes_part_2/iso_country=%22NA%22
234     468     airport_codes_part_2/iso_country=%22PR%22
120632  241264  airport_codes_part_2/iso_country=%22US%22

?????????????
Не понимаю почему в папке нет партиций
drwxr-xr-x   - student42_19 student42_19          0 2022-02-10 17:23 airport_codes_part_2/type=%22closed%22
drwxr-xr-x   - student42_19 student42_19          0 2022-02-10 17:23 airport_codes_part_2/type=%22heliport%22
drwxr-xr-x   - student42_19 student42_19          0 2022-02-10 17:23 airport_codes_part_2/type=%22seaplane_base%22
drwxr-xr-x   - student42_19 student42_19          0 2022-02-10 17:23 airport_codes_part_2/type=%22small_airport%22

создаються файлы по типам того поля которое в partition стоит первым
?????????????

следующая партиция находиться внутри 
[student42_19@bigdataanalytics-worker-3 ~]$ hdfs dfs -ls airport_codes_part_2/iso_country=%22MH%22
Found 1 items
drwxr-xr-x   - student42_19 student42_19          0 2022-02-10 17:37 airport_codes_part_2/iso_country=%22MH%22/type=%22small_airport%22
[student42_19@bigdataanalytics-worker-3 ~]$ hdfs dfs -ls airport_codes_part_2/iso_country=%22NA%22
Found 2 items
drwxr-xr-x   - student42_19 student42_19          0 2022-02-10 17:37 airport_codes_part_2/iso_country=%22NA%22/type=%22heliport%22
drwxr-xr-x   - student42_19 student42_19          0 2022-02-10 17:37 airport_codes_part_2/iso_country=%22NA%22/type=%22small_airport%22
[student42_19@bigdataanalytics-worker-3 ~]$ hdfs dfs -ls airport_codes_part_2/iso_country=%22PR%22
Found 2 items
drwxr-xr-x   - student42_19 student42_19          0 2022-02-10 17:37 airport_codes_part_2/iso_country=%22PR%22/type=%22heliport%22
drwxr-xr-x   - student42_19 student42_19          0 2022-02-10 17:37 airport_codes_part_2/iso_country=%22PR%22/type=%22small_airport%22
[student42_19@bigdataanalytics-worker-3 ~]$ hdfs dfs -ls airport_codes_part_2/iso_country=%22US%22
Found 4 items
drwxr-xr-x   - student42_19 student42_19          0 2022-02-10 17:37 airport_codes_part_2/iso_country=%22US%22/type=%22closed%22
drwxr-xr-x   - student42_19 student42_19          0 2022-02-10 17:37 airport_codes_part_2/iso_country=%22US%22/type=%22heliport%22
drwxr-xr-x   - student42_19 student42_19          0 2022-02-10 17:37 airport_codes_part_2/iso_country=%22US%22/type=%22seaplane_base%22
drwxr-xr-x   - student42_19 student42_19          0 2022-02-10 17:37 airport_codes_part_2/iso_country=%22US%22/type=%22small_airport%22
[student42_19@bigdataanalytics-worker-3 ~]$ hdfs dfs -ls airport_codes_part_2/iso_country=%22US%22/type=%22small_airport%22

 */

select `type`, iso_country 
FROM
(select `type`, iso_country, 
ROW_NUMBER() OVER (PARTITION BY `type` ORDER BY iso_country DESC) as rank
from airport_codes_part_2) ranked_v
where ranked_v.rank = 1 limit 1;

