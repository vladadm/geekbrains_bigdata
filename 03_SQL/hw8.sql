-- Удаляем базу student42_19 если она существует
drop database if exists student42_1 cascade;

-- Выводим список доуступных баз данных
show databases;
-- Выводим список доступных таблиц
show tables;

-- select 1 as numbe;

-- Создаем базу если она не существует
create database if not exists student42_19;

--зачем используем use?
-- переключаемся на базу student42_19
use student42_19;
-- Выводим список таблиц student42_19
show tables;

drop table if exists student42_19.airport_codes;
drop table if exists student42_19.airport_codes_part;

-- drop database if exists student42_19 cascade;

-- show databases;

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
row format delimited fields terminated by ',' --ESCAPED BY '"'
stored as textfile
location "/user/student42_1/airports"
tblproperties ("skip.header.line.count"="1");

show tables;

select count(distinct `type`) from airport_codes;

create external table airport_codes_part (
    id int,
    ident string,
--    `type` string,
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
row format delimited fields terminated by ',' --ESCAPED BY '"'
stored as textfile
location "/user/student42_19/airports_code_parts"
tblproperties ("skip.header.line.count"="1");

show create table airport_codes;
show create table airport_codes_part;

show tables;

select MAP(123,'qwe', 345,'ooo') as dictionary;
select ARRAY(1,2,3) as list;