drop table image;
drop table text;
drop table video;
drop table has;
drop table data_object;
drop table ownership;
drop table contained_in;
drop table is_in;
drop table cell;
drop table sheets;
drop table documents;
drop table users;

create table users
	(username		varchar(20),
	 password		varchar(20) check (length(password) >= 8),
	 name		    varchar(20) not null,
	 email_id   	varchar(20) not null,
	 primary key (username)
	);

create table documents
	(doc_id			integer check (doc_id >= 0),
	 doc_name		varchar(20) not null,
	 created_on		timestamp,
	 created_by		varchar(20),  
	 primary key (doc_id),
	 foreign key (created_by) references users
	 	on delete cascade
	);

create table sheets
	(sheet_id		integer check (sheet_id >= 0), 
	 sheet_name		varchar(20) not null, 
	 total_columns	integer check (total_columns > 0),
	 total_rows		integer check (total_rows > 0),
	 sheet_last_modified	timestamp,
	 sheet_created_on	timestamp,
	 primary key (sheet_id)
	);

create table cell
	(cell_id		integer check (cell_id >= 0), 
	 cell_x			integer not null, 
	 cell_y			integer not null, 
	 cell_color		varchar(20),
	 primary key (cell_id)
	);

create table data_object
	(data_id		integer check(data_id >= 0), 
     data_size		integer check(data_size >= 0),
     data_type		varchar(20) check(data_type in ('image','text','video')),
	 primary key (data_id)
	);

create table image
	(data_id		integer,
	 image_data		oid,
	 image_title	varchar(20),
	 primary key (data_id),
	 foreign key (data_id) references data_object
		on delete cascade
	);

create table text
	(data_id		integer,
	 text_data		varchar(1000),
	 text_font		varchar(20),
	 font_size		integer check(font_size > 0),
	 text_color		varchar(20),
	 primary key (data_id),
	 foreign key (data_id) references data_object
		on delete cascade
	);

create table video
	(data_id		integer,
	 video_data		oid,
	 video_title	varchar(20),
	 primary key (data_id),
	 foreign key (data_id) references data_object
		on delete cascade
	);

create table ownership
	(username		varchar(20),
	 doc_id			integer check(doc_id >= 0),
	 rights 		varchar(20) check(rights in ('read','admin','edit')),
	 primary key (username,doc_id),
	 foreign key (username) references users
		on delete cascade,
	 foreign key (doc_id) references documents
		on delete cascade
	);

create table contained_in
	(doc_id			integer check(doc_id >= 0),
	 sheet_id		integer check(sheet_id >= 0),
	 primary key (sheet_id,doc_id),
	 foreign key (sheet_id) references sheets
		on delete cascade,
	 foreign key (doc_id) references documents
		on delete cascade
	);

create table is_in
	(sheet_id		integer check(sheet_id >= 0),
	 cell_id		integer check(cell_id >= 0),
	 primary key (sheet_id,cell_id),
	 foreign key (sheet_id) references sheets
		on delete cascade,
	 foreign key (cell_id) references cell
		on delete cascade
	);

create table has
	(data_id		integer check(data_id >= 0),
	 cell_id		integer check(cell_id >= 0),
	 primary key (cell_id,data_id),
	 foreign key (cell_id) references cell
		on delete cascade,
	 foreign key (data_id) references data_object
		on delete cascade
	);