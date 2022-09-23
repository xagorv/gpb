# gpb
Test task by Val Gorokhov

## Cloning repository
git clone https://github.com/xagorv/gpb.git

Starting database
cd gpb
cd db
docker-compose -f stack.yml up
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' db_db_1
I got here 172.18.0.2

## Connect to database:
mysql -h 172.18.0.2 -P 3306 -u root -p
Password is 'example'

## Create database:

CREATE DATABASE logger;
use logger

CREATE TABLE message (
created TIMESTAMP(0) NOT NULL,
id VARCHAR(16) NOT NULL,
int_id CHAR(16) NOT NULL,
str VARCHAR(255) NOT NULL,
status BOOL,
CONSTRAINT message_id_pk PRIMARY KEY(id)
);

CREATE INDEX message_created_idx ON message (created);
CREATE INDEX message_int_id_idx ON message (int_id);

CREATE TABLE log (
created TIMESTAMP(0) NOT NULL,
int_id CHAR(16) NOT NULL,
str VARCHAR(32),
address VARCHAR(255)
);

CREATE INDEX log_address_idx USING hash ON log (address);


