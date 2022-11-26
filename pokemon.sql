create database titanic_database;

create table titanic_database.titanic_passengers(
	passenger_id int primary key,
	survived varchar(255),
	pclass varchar(255),
	name varchar(255),
	sex varchar(255),
	age varchar(255),
	sibsp varchar(255),
	parch varchar(255),
	ticket varchar(255),
	fare varchar(255),
	cabin varchar(255),
	embarked varchar(255)
);