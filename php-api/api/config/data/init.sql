DROP DATABASE if exists zgang;
DROP USER if exists 'zgang'@localhost;
/* database */
CREATE DATABASE zgang;
use zgang;
/* default user and pswd */
CREATE USER 'zgang'@localhost IDENTIFIED BY PASSWORD '*A63BAD3201B2E31FF52C79242F27D2A3FCD99499';
GRANT ALL PRIVILEGES ON zgang.* TO 'zgang'@localhost;
FLUSH PRIVILEGES;
