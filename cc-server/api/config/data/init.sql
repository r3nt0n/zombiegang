DROP DATABASE if exists zgang;
DROP USER if exists 'zgang'@'%';
/* database */
CREATE DATABASE zgang;
use zgang;
/* default user and pswd */
CREATE USER 'zgang'@'%' IDENTIFIED BY "changethispassword";
GRANT ALL PRIVILEGES ON zgang.* TO 'zgang'@'%';
FLUSH PRIVILEGES;
