create database drones;
use drones;
create table point(id int(11) unsigned auto_increment primary key not null,x int(16) not null,y int(16) not null,z int(16) not null,transitpoint bool not null);
insert into point(x,y,z,transitpoint) values(0,0,0,1);
insert into point(x,y,z,transitpoint) values(1,1,0,1);
insert into point(x,y,z,transitpoint) values(1,2,0,0);
insert into point(x,y,z,transitpoint) values(2,2,0,1);
insert into point(x,y,z,transitpoint) values(4,3,0,0);
create table drone(id int(11) unsigned auto_increment primary key not null,droneid int(11) not null, x int(16) not null,y int(16) not null, z int(16) not null);
insert into drone(droneid,x,y,z) values(0,1,1,2)
