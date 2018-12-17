create database drones;
use drones;
create table point(id int(11) unsigned auto_increment primary key not null,pointID int(16) not null,x int(16) not null,y int(16) not null,z int(16) not null,transitpoint bool not null);
insert into point(pointID, x,y,z,transitpoint) values(0,0,0,0,1);
insert into point(pointID, x,y,z,transitpoint) values(1,1,0,0,1);
insert into point(pointID, x,y,z,transitpoint) values(2,2,0,0,0);
insert into point(pointID, x,y,z,transitpoint) values(3,3,0,0,0);
insert into point(pointID, x,y,z,transitpoint) values(4,4,0,0,1);
insert into point(pointID, x,y,z,transitpoint) values(5,5,0,0,1);
create table drone(id int(11) unsigned auto_increment primary key not null,droneID int(11) not null, x int(16) not null,y int(16) not null, z int(16) not null);
insert into drone(droneID,x,y,z) values(0,1,1,2)
