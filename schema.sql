CREATE DATABASE IF NOT EXISTS santhiram_clg;

USE santhiram_clg;

create table paper_publications (
	id int primary key auto_increment,
    submission_date date,
    user_name varchar(30),
    file_content longblob,
    file_name varchar(100),
    author_name varchar(50),
    title varchar(500),
    abstract varchar(500),
    keywords varchar(500)
    )
