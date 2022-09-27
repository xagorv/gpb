# gpb
Test task by Val Gorokhov

## Cloning repository
git clone https://github.com/xagorv/gpb.git

## Starting database
cd gpb
cd db
docker run -d --restart always --network host --name mariadb --env MARIADB_ROOT_PASSWORD=example mariadb

## Connect to database:
mysql -P 3306 -u root -p
Password is 'example'

## Create database:

CREATE DATABASE logger;
use logger

CREATE TABLE message (
created TIMESTAMP(0) NOT NULL,
id VARCHAR(100) NOT NULL,
int_id CHAR(16) NOT NULL,
str VARCHAR(255) NOT NULL,
address VARCHAR(255),
status BOOL,
CONSTRAINT message_id_pk PRIMARY KEY(id)
);

CREATE INDEX message_created_idx ON message (created);
CREATE INDEX message_int_id_idx ON message (int_id);

CREATE TABLE log (
created TIMESTAMP(0) NOT NULL,
int_id CHAR(16) NOT NULL,
str VARCHAR(600),
address VARCHAR(255)
);

CREATE INDEX log_address_idx USING hash ON log (address);

## Fill out database:
cd gpb/bin
./process.pl

## Start Apache servcer
cd /gpb/docker_apache
docker build -t docker_apache .

cd gpb/
docker run -v `pwd`/httpd:/var/www/html --name apache --network host -d docker_apache /usr/sbin/apache2ctl -D FOREGROUND


