drop table if exists dir_task; 
create table dir_task
(
	task_id  bigint NOT NULL PRIMARY KEY AUTO_INCREMENT ,
	file_id int not null,
	filename  varchar(255) not null,
	server_shell varchar(255) ,
	server_param varchar(255),
	client_ip varchar(50) not null,
	client_port int,
	client_shell varchar(255) ,
	client_param varchar(255),
	day varchar(20) not null,
	hour int default -1 ,
	exist boolean not null,
	notify int default -1 ,
	status int default -1
   
);


drop table if exists dir_metadata;
create table dir_metadata
(
    file_id int not null primary key auto_increment,
	filereg varchar(255) not null,
	server_shell varchar(255) ,
	server_param varchar(255),
	cacul_period varchar(10) default 'day',
	client_ip varchar(50) not null,
	client_port int,
	client_shell varchar(255) ,
	client_param varchar(255)
	
);

insert into dir_metadata (file_id, filereg, server_shell, server_param, cacul_period, client_ip, client_port, client_shell,client_param)
values('/home/conny/.xinputrc${day}','day','10.0.0.1','8088','/home/conny/a.sh','${day}');
insert into dir_task(filename, client_ip, client_port, client_shell, client_param, day, hour) 
select filereg, client_ip, client_port, client_shell, client_param from dir_metadata where cacul_period ="hour"
values('/home/conny/.xinputrc20141128', '20.10.2.1', 8088, 'sbc.sh', 'abc', '20141128', 12   )

select distinct client_ip ,client_port from dir_metadata
select * from dir_task where status=-1

select count(file_id) from dir_task  where  day=%s and hour=%s
select count(*) from dir_metadata and cacul_period='hour'
