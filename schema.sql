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
    );

CREATE TABLE IF NOT EXISTS users (

        id bigint NOT NULL,
        username VARCHAR(150) NOT NULL,
        password VARCHAR(500) NOT NULL,
        user_role char(50) NOT NULL DEFAULT 'normal_user',
        PRIMARY KEY(id)
);
