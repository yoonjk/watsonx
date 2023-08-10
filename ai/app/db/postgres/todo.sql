DROP TABLE IF EXISTS users;

CREATE TABLE users(
	id serial,
	email varchar(45),
	username varchar(45),
	first_name varchar(45),
	last_name varchar(45),
	hashed_password varchar(200),
	is_active boolean,
	role varchar(45),
	primary key(id)
)

drop table if exists todos ;

CREATE TABLE todos(
	id serial,
	title varchar(200),
	description varchar(200),
	priority integer,
	complete boolean,
	owner_id integer, 
	primary key(id),
	foreign key(owner_id) references users(id)
)
