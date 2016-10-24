delete from image;
delete from text;
delete from video;
delete from has;
delete from data_object;
delete from ownership;
delete from contained_in;
delete from is_in;
delete from cell;
delete from sheets;
delete from documents;
delete from users;

insert into users values ('rawal', 'rawal12345', 'Rawal Khirodkar', 'rawalkhirodkar@gmail.com');
insert into users values ('rawal1', 'rawal12345', 'Rawal Khirodkar', 'rawalkhirodkar@gmail.com');
insert into users values ('rawal2', 'rawal12345', 'Rawal Khirodkar', 'rawalkhirodkar@gmail.com');
insert into users values ('rawal3', 'rawal12345', 'Rawal Khirodkar', 'rawalkhirodkar@gmail.com');

insert into documents values ('1', 'Name1', '20/02/1995','Rawal');
insert into documents values ('2', 'Name2', '20/02/1995','Rawal2');
insert into documents values ('3', 'Name3', '20/02/1995','Rawal3');

insert into sheets values ('1', 'Sheet1','2','3','20/02/2013','20/02/1995');
insert into sheets values ('2', 'Sheet2','2','3','20/02/2014','20/02/1995');
insert into sheets values ('3', 'Sheet3','2','3','20/02/2015','20/02/1995');
	
insert into cells values ('1', '0','0','White');
insert into cells values ('2', '1','0','White');
insert into cells values ('3', '2','0','White');
insert into cells values ('4', '3','0','White');
insert into cells values ('5', '4','0','White');
insert into cells values ('6', '5','0','White');
insert into cells values ('7', '6','0','White');


insert into ownership values ('rawal12345','1','edit')
insert into ownership values ('rawal12345','2','edit')
insert into ownership values ('rawal12345','3','edit')


insert into contained_in values ('1','1')
insert into contained_in values ('1','2')
insert into contained_in values ('1','3')

insert into is_in values ('1','1')
insert into is_in values ('2','1')
insert into is_in values ('3','1')
insert into is_in values ('4','1')
