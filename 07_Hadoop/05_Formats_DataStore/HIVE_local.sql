show databases;

drop database if exists my_test_db cascade;
drop database if exists mydb cascade;

create database my_test_db;
create database mydb;

show databases;

/*
root@e18b592c991f:/# hdfs dfs -ls /user/hive/warehouse/
Found 2 items
drwxrwxr-x   - root supergroup          0 2022-02-11 11:23 /user/hive/warehouse/my_test_db.db
drwxrwxr-x   - root supergroup          0 2022-02-11 11:24 /user/hive/warehouse/mydb.db

 */

use my_test_db;

drop table if exists my_test_tab;

show tables;

/*
root@e18b592c991f:/# echo -e "1,2\n3,4\n5,6" > test_datafile.txt
root@e18b592c991f:/# cat test_datafile.txt
1,2
3,4
5,6

root@e18b592c991f:/# hdfs dfs -put test_datafile.txt /user/hive/warehouse/my_test_db.db/test_file
root@e18b592c991f:/# hdfs dfs -cat /user/hive/warehouse/my_test_db.db/test_file
1,2
3,4
5,6
 */


create temporary external table my_test_table (
    col_1 int,
    col_2 int
)
row format delimited fields terminated by ',' -- указываем разделитель |
stored as TEXTFILE  -- формат хранения 
location "/user/hive/warehouse/my_test_db.db/";

select * from my_test_table;

/*
 root@e18b592c991f:/# hdfs dfs -du /user/hive/warehouse/mydb.db
12  /user/hive/warehouse/mydb.db/test_file
 */

-----------------------------------
-----------------------------------
/*
root@e18b592c991f:/# hdfs dfs -put uber-raw-data-janjune-15.csv /user/hive/warehouse/mydb.db/uber-data-janjune-15

root@e18b592c991f:/# hdfs dfs -du -h /user/hive/warehouse/mydb.db
526.1 M  /user/hive/warehouse/mydb.db/uber-data-janjune-15
 */
use mydb;
drop table if exists uber_data_ex;

create external table uber_data_ex (
	Dispatching_base_num string,
	Pickup_date timestamp,
	Affiliated_base_num string,
	locationID int
)
row format delimited fields terminated by ','
stored as TEXTFILE
location "/user/hive/warehouse/mydb.db/"
tblproperties ("skip.header.line.count"="1")
--SERDEPROPERTIES("timestamp.formats"="yyyy-MM-dd HH:mm:ss")
;

show tables;

SELECT * from uber_data_ex limit 10;

show create table uber_data_ex;

select count(1) from uber_data_ex; -- 8 sec

select count(locationID) from uber_data_ex; -- 10 sec

select count(distinct dispatching_base_num) from uber_data_ex; -- 11 sec

--CSV
create table uber_data_ex_csv
	(
	Dispatching_base_num string,
	Pickup_date timestamp,
	Affiliated_base_num string,
	locationID int
)
row format delimited fields  terminated by ","
stored as textfile;

insert overwrite table uber_data_ex_csv
select * from uber_data_ex;

/*
root@e18b592c991f:/# hdfs dfs -du -h /user/hive/warehouse/mydb.db
526.1 M  /user/hive/warehouse/mydb.db/uber-data-janjune-15
512.5 M  /user/hive/warehouse/mydb.db/uber_data_ex_csv
 */

select * from uber_data_ex_csv limit 10;

select count(1) from uber_data_ex_csv; -- 3 sec
select count(locationID) from uber_data_ex_csv; -- 10 sec
select count(distinct dispatching_base_num) from uber_data_ex_csv; -- 11 sec

-- SQ
create table uber_data_ex_sq
	(
	Dispatching_base_num string,
	Pickup_date timestamp,
	Affiliated_base_num string,
	locationID int
)
stored as sequencefile;

insert overwrite table uber_data_ex_sq
select * from uber_data_ex;

/*
root@e18b592c991f:/# hdfs dfs -du -h /user/hive/warehouse/mydb.db
526.1 M  /user/hive/warehouse/mydb.db/uber-data-janjune-15
512.5 M  /user/hive/warehouse/mydb.db/uber_data_ex_csv
682.5 M  /user/hive/warehouse/mydb.db/uber_data_ex_sq
 */

select * from uber_data_ex_sq limit 10;

select count(1) from uber_data_ex_sq; -- 2 sec
select count(locationID) from uber_data_ex_sq; -- 40 sec
select count(distinct dispatching_base_num) from uber_data_ex_sq; -- 42 sec


--PARQUET
create table uber_data_ex_pq
	(
	Dispatching_base_num string,
	Pickup_date timestamp,
	Affiliated_base_num string,
	locationID int
)
stored as parquet;

insert overwrite table uber_data_ex_pq
select * from uber_data_ex;

/*
root@e18b592c991f:/# hdfs dfs -du -h /user/hive/warehouse/mydb.db
526.1 M  /user/hive/warehouse/mydb.db/uber-data-janjune-15
512.5 M  /user/hive/warehouse/mydb.db/uber_data_ex_csv
188.4 M  /user/hive/warehouse/mydb.db/uber_data_ex_pq
682.5 M  /user/hive/warehouse/mydb.db/uber_data_ex_sq
 */

select * from uber_data_ex_pq limit 10;

select count(1) from uber_data_ex_pq; -- 2.8 sec
select count(locationID) from uber_data_ex_pq; -- 6.6 sec
select count(distinct dispatching_base_num) from uber_data_ex_pq; -- 6.6 sec

-- пока лидер как по объему занятого пространства так и по скорости выполнения выборки --


--ORC
create table uber_data_ex_orc
	(
	Dispatching_base_num string,
	Pickup_date timestamp,
	Affiliated_base_num string,
	locationID int
)
stored as orc;

insert overwrite table uber_data_ex_orc
select * from uber_data_ex;

/*
root@e18b592c991f:/# hdfs dfs -du -h /user/hive/warehouse/mydb.db
526.1 M  /user/hive/warehouse/mydb.db/uber-data-janjune-15
512.5 M  /user/hive/warehouse/mydb.db/uber_data_ex_csv
36.5 M   /user/hive/warehouse/mydb.db/uber_data_ex_orc
188.4 M  /user/hive/warehouse/mydb.db/uber_data_ex_pq
682.5 M  /user/hive/warehouse/mydb.db/uber_data_ex_sq
 */

select count(1) from uber_data_ex_orc; -- 2.8 sec
select count(locationID) from uber_data_ex_pq; -- 5.6 sec
select count(distinct dispatching_base_num) from uber_data_ex_orc; -- 7.7

-- совсем немного быстрее паркета, но в разы меньше занимаемом месте на диске --

--AVRO
create table uber_data_ex_avro
	(
	Dispatching_base_num string,
	Pickup_date timestamp,
	Affiliated_base_num string,
	locationID int
)
stored as avro;

insert overwrite table uber_data_ex_avro
select * from uber_data_ex;

/*
root@e18b592c991f:/# hdfs dfs -du -h /user/hive/warehouse/mydb.db
526.1 M  /user/hive/warehouse/mydb.db/uber-data-janjune-15
351.2 M  /user/hive/warehouse/mydb.db/uber_data_ex_avro
512.5 M  /user/hive/warehouse/mydb.db/uber_data_ex_csv
36.5 M   /user/hive/warehouse/mydb.db/uber_data_ex_orc
188.4 M  /user/hive/warehouse/mydb.db/uber_data_ex_pq
682.5 M  /user/hive/warehouse/mydb.db/uber_data_ex_sq
 */

select * from uber_data_ex_avro limit 10;

select count(1) from uber_data_ex_avro; -- 2.6 sec
select count(locationID) from uber_data_ex_avro; -- 45 sec
select count(distinct dispatching_base_num) from uber_data_ex_avro; -- 47 sec

-- занимает на 15% мнеьше места чем text|csv, но значительно медленнее.

/* Сжатие PARQUET */
/* UNCOMPRESSED, GZIP or SNAPPY */

-- SNAPPY

set parquet.compression=SNAPPY;

CREATE TABLE testsnappy_pq
STORED AS PARQUET
AS SELECT * FROM uber_data_ex;

/*
root@e18b592c991f:/# hdfs dfs -du -h /user/hive/warehouse/mydb.db |grep 15
526.1 M  /user/hive/warehouse/mydb.db/uber-data-janjune-15

root@e18b592c991f:/# hdfs dfs -du -h /user/hive/warehouse/mydb.db |grep pq
66.7 M   /user/hive/warehouse/mydb.db/testsnappy_pq
188.4 M  /user/hive/warehouse/mydb.db/uber_data_ex_pq
 */

select count(1) from testsnappy_pq; -- 3.1 sec
select count(locationID) from testsnappy_pq; -- 5.7 sec
select count(distinct dispatching_base_num) from testsnappy_pq; -- 6.6 sec

-- GZIP

set parquet.compression=GZIP;

CREATE TABLE testgzip_pq
STORED AS PARQUET
AS SELECT * FROM uber_data_ex;

/*
root@e18b592c991f:/# hdfs dfs -du -h /user/hive/warehouse/mydb.db |grep 15
526.1 M  /user/hive/warehouse/mydb.db/uber-data-janjune-15

root@e18b592c991f:/# hdfs dfs -du -h /user/hive/warehouse/mydb.db |grep pq
50.6 M   /user/hive/warehouse/mydb.db/testgzip_pq
66.7 M   /user/hive/warehouse/mydb.db/testsnappy_pq
188.4 M  /user/hive/warehouse/mydb.db/uber_data_ex_pq
 */

-- GZIP сжимает более чем в 10 раз от исходного размера !!! --

select count(1) from testgzip_pq; -- 2.6 sec
select count(locationID) from testgzip_pq; -- 5.5 sec
select count(distinct dispatching_base_num) from testgzip_pq; -- 6.6 sec

-- в случае с PARQUET сжатие GZIP эффективнее SNYPPY


/* Сжатие ORC */
/* NONE, ZLIB or SNAPPY */


-- SNAPPY

CREATE TABLE testsnappy_orc
STORED AS ORC
TBLPROPERTIES("orc.compress"="snappy")
AS SELECT * FROM uber_data_ex;

/*
root@e18b592c991f:/# hdfs dfs -du -h /user/hive/warehouse/mydb.db |grep 15
526.1 M  /user/hive/warehouse/mydb.db/uber-data-janjune-15

root@e18b592c991f:/# hdfs dfs -du -h /user/hive/warehouse/mydb.db |grep orc
48.6 M   /user/hive/warehouse/mydb.db/testsnappy_orc
36.5 M   /user/hive/warehouse/mydb.db/uber_data_ex_orc
 */

select count(1) from testsnappy_orc; -- 2.8 sec
select count(locationID) from testsnappy_orc; -- 6.6 sec
select count(distinct dispatching_base_num) from testsnappy_orc; -- 7.7 sec

-- ZLIB

CREATE TABLE testzlib_orc
STORED AS ORC
TBLPROPERTIES("orc.compress"="ZLIB")
AS SELECT * FROM uber_data_ex;

/*
root@e18b592c991f:/# hdfs dfs -du -h /user/hive/warehouse/mydb.db |grep 15
526.1 M  /user/hive/warehouse/mydb.db/uber-data-janjune-15

root@e18b592c991f:/# hdfs dfs -du -h /user/hive/warehouse/mydb.db |grep orc
48.6 M   /user/hive/warehouse/mydb.db/testsnappy_orc
36.5 M   /user/hive/warehouse/mydb.db/testzlib_orc
36.5 M   /user/hive/warehouse/mydb.db/uber_data_ex_orc
 */

select count(1) from testzlib_orc; -- 3 sec
select count(locationID) from testzlib_orc; -- 6.7 sec
select count(distinct dispatching_base_num) from testzlib_orc; -- 7.6 sec

-- в случае с ORC сжатие ZLIB эффективнее SNYPPY


-- drop table if exists testgzip_orc ;

-- drop database mydb cascade;

/*
format	            file size	select 1	select 2	select 3	select AVG
TEXTFILE			526.1		8			10			11			9,7
CSV					512.5		3			10			11			8,0
sequencefile		682.5		2			40			42			28,0
PARQUET				188.4		2,80		6,6			6,6			5,3
PARQUET with SNAPPY	66.7		3,1			5,7			6,6			5,1
PARQUET with GZIP	50.6		2,6			5,5			6,6			4,9
ORC					36.5		2,8			5,6			7,7			5,4
ORC with SNAPPY		48.6		2,8			6,6			7,7			5,7
ORC with ZLIB		36.5		3			6,7			7,6			5,8
AVRO				351.2		2,6			45			47			31,5
 */

/* 
 если важна скорость выполнения селектов:
 1 место PARQUET with GZIP avg: 4.9
 2 место PARQUET with SNAPPY avg: 5.1
 3 место делят PARQUET и ORC 5.3 vs 5.4
 аутсайдер AVRO
 
 если важно дисковое прастроанство:
 1 место делят ORC и ORC with ZLIB экономия дисквого пространства 93.06 % 
 2 место PARQUET with SNAPPY экономия дисквого пространства 90.76 % 
 3 место PARQUET with GZIP экономия дисквого пространства 90.38 %
 аутсайдер sequencefile 
 
 */


