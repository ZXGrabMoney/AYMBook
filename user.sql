drop table if exists user;
create table user (
  email string not null primary key,
  passwd string not null
);