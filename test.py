import  pymysql
#
#
#
# DORP TABLE IF EXISTS users;
# CREATE TABLE users (
#     id int(8) NOT Null AUTO_INCREMENT,
#     username varchar(255) default null,
#     email varchar(255) default null,
#     password varchar(255) default null,
#     primary key (id)
# ) engine=InnoDB default charset=utf8;
#
# drop table if exists airticles;
# create table airticles (
#     id int(8) not null auto_increment,
#     title varchar(255) default null,
#     content text,
#     author varchar(255) default null,
#     create_date datetime default null,
#     primary key (id)
# ) engine=InnoDB default charset=utf8;