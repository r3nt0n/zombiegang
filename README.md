<div id="top"></div>
<!-- 
This documentation was written using Best-README-Template by othneildrew
https://github.com/othneildrew
https://github.com/othneildrew/Best-README-Template 
Thanks dude :)
-->



<!-- PROJECT SHIELDS -->
![[Version 0.5.1~beta](https://github.com/r3nt0n)](http://img.shields.io/badge/version-0.5.1~beta-orange.svg)
![[Python 3](https://github.com/r3nt0n)](http://img.shields.io/badge/python-3-blue.svg)
![[GPL-3.0 License](https://github.com/r3nt0n)](https://img.shields.io/badge/license-GPL%203.0-brightgreen.svg)
![[Date](https://github.com/r3nt0n)](http://img.shields.io/badge/date-2022-yellow.svg)



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/r3nt0n/zombiegang">
    <img src="https://github.com/r3nt0n/zombiegang/blob/master/img/logo.svg" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">zombiegang</h3>

  <p align="center">
    The extensible botnet framework
    <br />
    <a href="#usage"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="#-getting-started">Kickoff</a>
    ·
    <a href="https://github.com/r3nt0n/zombiegang">Report Bug</a>
    ·
    <a href="https://github.com/r3nt0n/zombiegang">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of contents</summary>
  <ol>
    <li>
      <a href="#-about-the-project">📖 About the Project</a>
      <ul>
        <li><a href="#built-with">Built with</a></li>
      </ul>
    </li>
    <li>
      <a href="#-getting-started">✨ Getting started</a>
      <ul>
        <li><a href="#-download-and-setup">🚀 Download and setup</a></li>
        <li><a href="#-start-cc-server">🕸️ Start cc-server</a></li>
        <li><a href="#-start-zombie-client">🧟 Start zombie client</a></li>
        <li>
          <a href="#-start-master-client">🧙‍♂️ Start master client</a>
          <ul>
            <li><a href="#web-client">web client</a></li>
            <li><a href="#cli-client">cli client</a></li>
          </ul>
        </li>
      </ul>
    </li>
    <li>
      <a href="#-tools-and-attacks">🎨 Tools and attacks</a>
      <ul>
        <li><a href="#keylogger-module">Keylogger module</a></li>
      </ul>
    </li>
    <li><a href="#-roadmap">🚧 Roadmap</a></li>
    <li>
      <a href="#-contributing">🌍 Contributing</a>
      <!--
      <ul>
        <li><a href="#contributors">Contributors</a></li>
      </ul>
      -->
    </li>
    <li><a href="#-changelist">📋 Changelist</a></li>
    <li><a href="#-contact">📇 Contact</a></li>
    <li><a href="#-acknowledgments">💎 Acknowledgments</a></li>
    <li><a href="#-legal-disclaimer">⚖️ Legal disclaimer</a></li>
    <li><a href="#-license">📙 License</a></li>
  </ol>
</details>

[](#)

<!-- ABOUT THE PROJECT -->
## 📖 About the Project

Zombiegang is a botnet framework written mostly in Python and PHP. It supports **asynchronous communication between cc and zombies**, **remote-shell** live sessions and **task scheduler**. It also has a **plugin manager**, which comes with some modules pre-included to perform most typical attacks (**DDoS, bruteforce** and **keylogger**). This modular approach allows anyone to **extend features by writing his own modules** (I will appreciate any contribution).  

<br>
<p align="center"><img src="https://github.com/r3nt0n/zombiegang/blob/master/img/intro2.gif" /></p>  

<br>

The **Command and Control server** is a semi-CRUD API written in php, which manages database read/write operations and authentication. This schema also allows to separate the front-end, which resides entirely in the client used by masters. 

Several kind of clients could be used to admin the botnet, and several kind of "zombie-clients" could co-exists too.
+ **master clients:** cli and web-based. The webclient is a light flask app focused on browse db info and schedule tasks. The cli client is intended to run remote-shell live sessions with one or more zombies simultaneously. Both of them support proxy configuration to reach cc-server anonymously.
+ **zombie clients:** by now, we only have a python client. Take note that you can write a zombie in the programming language of your preference, you just need to write a simple http client to communicate with API and maybe add some "zombie routines" (you can take the python client as an example). Again, any contribution would be welcome.   


Having a centralized db makes it easier for masters and zombies to exchange information asynchronously, removing the requirement of both being online at the same time.

<br>
<p align="center"><img src="https://github.com/r3nt0n/zombiegang/blob/master/img/attack_example.png" /></p>
<br>

You can schedule tasks and the zombies will receive this info as soon as they go online and refresh his "assignments". If the task was scheduled to be executed in future, the zombie will save this homework and run the task when the start time comes. You also can schedule stop datetimes.
  
There are special fields in DB which are designed to be nested values, so you can create new fields inside without touching any config (e.g.: `Tasks.task_content`,`Zombies.sysinfo`)  
  
<br>
<div align="center"><img src="https://github.com/r3nt0n/zombiegang/blob/master/img/zombies_info.gif" /><p style="font-decoration: italic;">zombie report example</p></div>  
<br>

### Built with

* [![PHP][PHP-badge]][PHP-url]
* [![MariaDB][MariaDB-badge]][MariaDB-url]
* [![Python][Python-badge]][Python-url]
* [![Flask][Flask-badge]][Flask-url]
* [![Jinja][Jinja-badge]][Jinja-url]
* [![JavaScript][JavaScript-badge]][JavaScript-url]
* [![Jquery][Jquery-badge]][Jquery-url]

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## ✨ Getting started

This is just a simple way to kickstart all the initial stuff. Obviously, in production environments you can use separate servers for DB and CC, and replace the http server for something like Apache or Nginx.

### 🚀 Download and setup

#### Download zombiegang framework
```shell
git clone https://github.com/r3nt0n/zombiegang.git
```

#### Create database
 
```shell
# step 1 and 2 are optional, only if mariadb not installed yet
sudo apt-get install mariadb-server, mariadb-client
sudo mysql_secure_installation
# change db default password and creates db structure
cd cc-server
nano api/config/data/init.sql
sudo ./initdb
```
#### Create your master profile
```shell
# log into mariadb with the password you just set in init.sql
mariadb -u zgang -p
use zgang;
insert into Masters SET username = '<your-username>', public_key = '<public-key>';
exit
```
***Note:** By now, when creating the new row you shouldn't specify any `password`, we will create it later. As another note, the `public_key` can be an empty string, since PKI logic isn't implemented yet.*
  
*Optional*: if you want to dump some mocked zombies into db for testing purposes, execute this file:
```shell
./dump-testdata
```

<p align="right">(<a href="#top">back to top</a>)</p>


### 🕸️ Start cc-server

Now you need to start the http server that will act as a proxy, allowing masters and zombies to interact with this db.

When editing `database.php`, you must set an IP/hostname pointing to db in `$host`, and the password you have just created to access it in `$password` (*optional*, if you changed db name and/or db user defaults, updates `$db_name` and `$db_user` too).

When editing `core.php`, you must change `$key` to a random string of your choice. This value is used for JWT tokens encode/decode operations. 

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

<p align="right">(<a href="#top">back to top</a>)</p>


### 🧟 Start zombie client
```shell
# install zombieclient dependencies 
cd zombie-client
pip install -r requirements.txt 

# to run the zombieclient
python3 run.py
```

You should have an output similar to this:

<div align="center"><img src="https://github.com/r3nt0n/zombiegang/blob/master/img/zombie_first_wakeup_example.png" /><p style="font-decoration: italic;">zombie first wake up</p></div>

Although it may seem like an error, this is expected behavior. Actually, the zombie has successfully created its user but, until we "allow it to enter", he will not be converted to zombie and will not be able to log in with that role into the cc server. We will cover how to ***accept*** zombies into the botnet using the master-client.

Zombies will send info about themselves on every boot and check regularly for new tasks, they just keep asking and serving to the cc-server forever (in fact, until you kill this process).

In real scenarios, you will also need persistence, obfuscation and probably compilation (since Python is not available by default on most systems).

<p align="right">(<a href="#top">back to top</a>)</p>


### 🧙‍♂️ Start master client
#### web client
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

**Note**: Mozilla Firefox and Chromium are the recommended browsers, any other could work but won't be officially supported. Some visual features (e.g.: emojis, form elements...) could vary across different browsers.

<br>
<div align="center"><img src="https://github.com/r3nt0n/zombiegang/blob/master/img/menu.png" /></div>
<br>

If you go to zombies section, you can see the new zombie requests to join the botnet that are awaiting your reply and the lists of zombies already joined. Here is where we can accept the zombie created before.

<br>
<div align="center"><img src="https://github.com/r3nt0n/zombiegang/blob/master/img/invocation_example.png" /></div>
<br>

If you want to cover your trace, use the built-in proxy tool to connect to cc-server through the socks5 proxy of your choice:

<br>
<div align="center"><img src="https://github.com/r3nt0n/zombiegang/blob/master/img/proxy_example.png" /><p style="font-decoration: italic;">proxy configuration example</p></div>
<br>

#### cli client
Additionally, you have a cli client (keeping msfconsole style) to login to cc-server and run remote-shell live sessions with online zombies, you could also connect through a socks5 proxy (like in web-based client) setting `PXHOST` and `PXPORT` before `login`.
```shell
# to run the masterclient (cli)
python3 cli.py
```

<div align="center"><img src="https://github.com/r3nt0n/zombiegang/blob/master/img/master-client_cli_live_session_example.png" /><p style="font-decoration: italic;">simple cli live session example</p></div>
<br>


> ⚠️ zombiegang is still on **development phase**, some features wasn't tested under all possible scenarios yet. Any **reported bug** could be helpful.

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- TOOLS AND ATTACKS -->
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

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ROADMAP -->
## 🚧 Roadmap

- [ ] Fixing **bugs**
    - [ ] **brt module** implemented but still need to finish both master and zombie sides
- [ ] Improving **features**
    - [ ] Implement **tasks details** view in master 
    - [ ] Implement **keylogger on/off** manual switch
    - [ ] Implement **keylogger logs** view in master
- [ ] Extra features
    - [ ] Implement PKI for master and zombie authentication
    - [ ] Improve docs

See the [open issues](https://github.com/r3nt0n/zombiegang/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## 🌍 Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

*For more information, please check the **[contribution guidelines page](https://github.com/r3nt0n/zombiegang/blob/master/CONTRIBUTING.md)**.*

[//]: # (### Contributors)

[//]: # (* [user-example]&#40;https://github.com/user-example&#41; what contribution?)

[//]: # ()
[//]: # (Thank you all!)

<p align="right">(<a href="#top">back to top</a>)</p>



## 📋 Changelist
+ `last development version (available on Github)`
  + Improving doc style
  + CONTRIBUTING.md created
  + Refactoring zombie-client to more efficient task result reporting
  + Task stop point scheduling implemented and working
  + Bruteforce attacks (ssh module) implemented but still need to finish both master and zombie sides
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
  + improving zombie structure, first scratches on zgang-console and remote shell live sessions
  + extending zombie-client brain operations: task scheduler, task manager, plugin manager and data models to create custom tasks implemented). in cc-api: missions operations extendented, improving db configuration (trigger to update manual stop in missions if update in task)
  + master-client: flask-wtf implemented, ddos attacks filter and creation implemented, improving templates and general project structure, desktop icons and xp blue/aeros taskbar added. cc-api: tasks and missions logic implemented, improving db configuration (foreign keys to link missions with tasks, trigger to update zombies ip and country codes after insert on AccessLogs)
  + zombie-client: basic autosetup operations implemented (write, load and generate settings/credentials), first scratch on threads
  + master-client: app factory and blueprints implemented, trying to implement flask-wtf
  + in master-client: improving structure,responsive design implemented, jquery and ajax implemented, add some javascript functions, proxy configuration implemented, welcome-notifications zombies logic implemented. php-api almost finished, first scratches with zombie client
  + flask-client: structuring windows and forms, ddos and brute attacks forms implemented
  + header added, launchers moved to central panel
  + table resizable and checkboxes logic implemented + aoe icons + gothicpixel font
  + first commit - php-api: jwt-auth and CRUD operations implemented. flask-client: basic features

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## 📇 Contact

r3nt0n: [Github](https://github.com/r3nt0n) - [email](r3nt0n@protonmail.com)  
zombiegang: [Github](https://github.com/r3nt0n/zombiegang)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## 💎 Acknowledgments

* [php-jwt](https://github.com/firebase/php-jwt) module
* Javascript code for resizable table found [here](https://www.brainbell.com/javascript/making-resizable-table-js.html)
* [Pixel Gothic font](https://dafonttop.com/pixel-gothic-font.font) by [Kajetan Andrzejak](https://dafonttop.com/tags.php?key=Kajetan%20Andrzejak)
* Verily Serif Mono by Stephen G. Hartke
* CSS sheet is based on <a href="https://github.com/jdan/98.css/blob/master/LICENSE">css win98</a> by <a href="https://github.com/jdan/">Jordan Scales</a>
* Age of Empires icons found <a href="https://www.forgottenempires.net/age-of-empires-ii-definitive-edition/campaigns">here</a>
* mIRC icon designed by [Pixel perfect](https://www.flaticon.es/autores/pixel-perfect)
* All pictures were found on the Internet

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- LEGAL DISCLAIMER -->
## ⚖️ Legal disclaimer
This is a personal project, and is created for the sole purpose of security awareness and education, it should not be used against systems that you do not have permission to test/attack. The author is not responsible for misuse or for any damage that you may cause. You agree that you use this software at your own risk. I don't own the rights of any image included, is just a funny tribute to some iconic legends (if you are the owner of any resource and want it to be removed, please contact me and I will do as soon as posible). You can't distribute this app with commercial purposes.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- LICENSE -->
## 📙 License

Distributed under the GNU General Public License v3.0. See `LICENSE` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[Flask-badge]: https://img.shields.io/badge/Flask-58c71c?logo=flask&style=for-the-badge&logoColor=white
[PHP-badge]: https://img.shields.io/badge/PHP-darkblue?logo=php&style=for-the-badge&logoColor=white
[Python-badge]: https://img.shields.io/badge/Python-blue?logo=python&style=for-the-badge&logoColor=white
[MariaDB-badge]: https://img.shields.io/badge/MariaDB-db259c?logo=mariadb&style=for-the-badge&logoColor=white
[Jinja-badge]: https://img.shields.io/badge/Jinja-d61515?logo=jinja&style=for-the-badge&logoColor=white
[JavaScript-badge]: https://img.shields.io/badge/JavaScript-efd81d?logo=javascript&style=for-the-badge&logoColor=black
[jQuery-badge]: https://img.shields.io/badge/jQuery-blueviolet?logo=jquery&style=for-the-badge&logoColor=white
[Flask-url]: https://flask.palletsprojects.com/en/2.2.x/
[PHP-url]: https://www.php.org
[Python-url]: https://www.python.org
[MariaDB-url]: https://www.mariadb.org
[Jinja-url]: https://
[JavaScript-url]: https://www.javascript.com
[jQuery-url]: https://www.jquery.com
