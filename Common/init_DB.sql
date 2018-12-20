drop database drones;
create database drones;
use drones;
create table points(
  id int(11) unsigned auto_increment primary key not null,
  pointID int(16) not null,
  x float not null,
  y float not null,
  z float not null
);

insert into points(pointID, x,y,z) values(0,0,0,0);
insert into points(pointID, x,y,z) values(1,1,0,0);
insert into points(pointID, x,y,z) values(2,2,0,0);
insert into points(pointID, x,y,z) values(3,3,0,0);
insert into points(pointID, x,y,z) values(4,4,0,0);
insert into points(pointID, x,y,z) values(5,5,0,0);

create table drones(
  id int(11) unsigned auto_increment primary key not null,
  droneID int(11) not null,
  unique_msg char(25) not null,
  x float not null,
  y float not null,
  z float not null
);
