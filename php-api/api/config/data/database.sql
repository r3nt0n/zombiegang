use zgang;
CREATE TABLE Users (
id int(11) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
username varchar(255) NOT NULL UNIQUE,
pswd varchar(60) NOT NULL
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
os varchar(255) NOT NULL,
current_public_ip varchar(15) NOT NULL,
current_hostname varchar(255) NOT NULL,
current_mac_addr varchar(255) NOT NULL,
refresh_secs DOUBLE(8,1) UNSIGNED DEFAULT 10.5
);
CREATE TABLE AccessLogs (
id int(11) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
date_time timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
successful BOOLEAN NOT NULL,
username varchar(255) NOT NULL,
public_ip varchar(15) NOT NULL,
hostname varchar(255),
mac_addr varchar(17)
);
CREATE TABLE Tasks (
id int(11) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
master_username varchar(255) NOT NULL,
task varchar(255) NOT NULL,
task_type varchar(255) NOT NULL,
submit_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
to_exec_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
to_stop_at timestamp DEFAULT CURRENT_TIMESTAMP,
zombie_username varchar(255) NOT NULL,
result varchar(2048),
exec_at timestamp
);