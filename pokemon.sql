create database pokemon_database;

create table pokemon_database.pokemon(
	id int primary key,
	name varchar(255),
	past_types int,
	height int,
	weight int,
	moves int
);