CREATE TABLE users(
	id int(11) NOT NULL AUTO_INCREMENT,
	email varchar(45),
	username varchar(45),
	first_name varchar(45),
	last_name varchar(45),
	hashed_password varchar(200),
	is_active int(1),
	role varchar(45),
	primary key(id)
) ENGINE=InnoDB AUTO_INCREMENT=1;

drop table if exists todos ;

CREATE TABLE todos(
	id int(11) NOT NULL AUTO_INCREMENT,
	title varchar(200),
	description varchar(200),
	priority int(1),
	complete int(1),
	owner_id int(11), 
	primary key(id),
	foreign key(owner_id) references users(id)
) ENGINE=InnoDB AUTO_INCREMENT=1;