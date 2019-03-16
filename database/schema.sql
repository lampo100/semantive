create table images(
  id integer primary key autoincrement,
  url varchar(255),
  tag varchar(255),
  content blob
);

create table texts(
  id integer primary key autoincrement,
  url varchar(255),
  tag varchar(255),
  content text
);

create table tasks(
  id varchar(36),
  url varchar(255),
  data_type varchar(255),
  tag varchar(255),
  active boolean
);