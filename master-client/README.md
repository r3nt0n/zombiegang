![[Version 0.1~beta](https://github.com/r3nt0n)](http://img.shields.io/badge/version-0.1~beta-orange.svg)
![[Python 3](https://github.com/r3nt0n)](http://img.shields.io/badge/python-3-blue.svg)
![[GPL-3.0 License](https://github.com/r3nt0n)](https://img.shields.io/badge/license-GPL%203.0-brightgreen.svg)
![[Date](https://github.com/r3nt0n)](http://img.shields.io/badge/date-2020-yellow.svg)


# zombiegang
zombiegang is a botnet written mostly in Python and PHP. It supports **asynchronous communication between cc and zombies**, **remote-shell** live sessions and **task scheduler**. It also has a **plugin manager**, which comes with some modules pre-included to perform the typical attacks (**DDoS, bruteforce** and **keylogger**). This modular approach allows anyone to **extend features by writing his own modules** (I will appreciate any contribution).    


The **Command and Control server** is a semi-CRUD API written in php, which manages database read/write operations and authentication. This schema also allows to separate the front-end, which resides entirely in the client used by masters. 

Several kind of clients could be used to admin the botnet, and several kind of "zombie-clients" could co-exists too.
+ **master clients:** cli and web-based. The webclient is a light flask app focused on browse db info and schedule tasks. The cli client is intended to run remote-shell live sessions with one or more zombies. Both of them support proxy configuration to reach cc-server anonymously.
+ **zombie clients:** by now, we only have a python client. Take note that you can write a zombie in the programming language of your preference, you just need to write a simple http client to communicate with API and maybe add some "zombie routines" (you can take the python client as an example). Again, any contribution would be welcome.   

<div align="center"><img src="https://github.com/r3nt0n/zombiegang/blob/master/img/master-client_cli_live_session_example.png" /><p style="font-decoration: italic;">simple cli live session example</p></div>


Having a centralized db makes it easier for masters and zombies to exchange information asynchronously, removing the requirement of both being online at the same time.

You can schedule tasks and the zombies will receive this info as soon as they go online and refresh his "assignments". If the task was scheduled to be executed in future, the zombie will save this homework and run the task when the start time comes. You also can schedule stop datetimes.

There are special fields in DB which are designed to be nested values, so you can create new fields inside without touching any config (e.g.: `Tasks.task_content`,`Zombies.sysinfo`)

**IMPORTANT NOTE:** zombiegang is still on development phase, some features wasn't tested under all possible scenarios yet. Any bug  reported could help.

## Get started
**Note:** This is just a simple way to kickstart all the initial stuff. Obviously, in production environments you can use separate servers for DB and CC, and replace the http server for something like Apache or Nginx. 

### Create database
 
```
sudo apt-get install mariadb-server, mariadb-client
sudo mysql_secure_installation
cd cc-server
# you should change db default password here:
nano api/config/data/init.sql
sudo ./initdb
```
**Create your master profile**
```
mariadb -u zgang -p
use zgang;
insert into Masters SET username = '<username>', public_key = '<public-key>';
```
***Note:** By now, you shouldn't specify any `password`, we will create it later. As another note, the `public_key` can be an empty string, since PKI logic isn't implemented yet.*
  
*Optional*: if you want to dump some mocked zombies into db for testing purposes:
```
./dump-testdata
```

### Start cc-server

```
cd cc-server
# Edit this file to match your db config
nano api/config/database.php
# and create your own secret-key
nano api/config/core.php 

# For testing purposes, you can use the simple http server provided by php
sudo php -S 127.0.0.1:8080
```

Now you should have the cc-server listening on port 8080 and connected to the database created before.

***Note:** You can disable masters access logging in `core.php`*


### Legal disclaimer
This is a personal project. I don't own the rights of any image included. You can't distribute this app with commercial purposes.

### References
+ Age of Empires icons found here https://www.forgottenempires.net/age-of-empires-ii-definitive-edition/campaigns
+ mIRC icon designed by <a href="https://www.flaticon.es/autores/pixel-perfect" title="Pixel perfect">Pixel perfect</a> from <a href="https://www.flaticon.es/" title="Flaticon"> www.flaticon.es  </a>  


