# AFPY Lyon Meetup
**RabbitMQ et Celery**

Ici vous trouverez le code et les diapositives du meetup *RabbitMQ et Celery* du 27 février 2019. Tout le code a été fait sur Python 3.6.

## Table of contents

- [Avant de commencer](#avant-de-commencer)
    - [Installation RabbitMQ](#installation-rabbit-mq)
    - [Installation requirements](#installation-requirements)
- [RabbitMQ](#rabbit-mq)
- [Celery](#celery)
- [Diapositives](#diapositives)

<a name="avant-de-commencer"/>

## Avant de commencer

<a name="installation-rabbit-mq"/>

### Installation RabbitMQ

L'installation de RabbitMQ peut varier en dépendant de votre système d'exploitation. Vous trouverez les instructions ici : [https://www.rabbitmq.com/download.html](https://www.rabbitmq.com/download.html).

<a name="installation-requirements"/>

### Installation requirements

Les répertoires ```rabbit``` et ```celery``` ont leur propre fichier ```requirements.txt```. La création d'un environnement virtuel est une façon simple de les installer.

Par exemple, pour le répertoire ```rabbit```:

```bash
> cd rabbit
> virtualenv -p python3 venv
...
> source venv/bin/activate
> pip install -r requirements.txt
...
```

La même séquence de commandes est à faire dans le répertoire ```celery```.

<a name="rabbit-mq"/>

## RabbitMQ

Le répertoire ```rabbit``` contient le code concernant la première partie du Meetup. Un ```producer.py``` envoie des messages au ```consumer.py```, ce dernier se mettant en boucle infinie pour les recevoir.

Vous pouvez lancer un ou plusieurs consumers en faisant ``` > python3 consumer.py```.

Pour envoyer des messages, lancez le producer avec ``` > python3 producer.py```

**consumer.py**
```bash
> python consumer.py
On attend des messages {-_-}
On a reçu ce message: b'Coucou !' (^_^)
```

**producer.py**
```bash
> python producer.py
Envoyé !
>
```

<a name="celery"/>

## Celery

Le répertoire Celery contient une application Django très basique (pas de base de données, pas de middleware, etc). Elle expose un endpoint ```/longRunningTask``` qui déclenche la tâche spécifiée sur ```views.py```. Les tâches sont déclarées dans ```tasks.py```.
`
**views.py**
```python
# Quelques tâches qu'on a défini dans tasks.py
from meetup.tasks import run_long_task
...

def task_view(request):
    """
    Cette view sera appelée à chaque requête arrivant sur "/longRunningTask".
    Vous pouvez ici remplacer "run_long_task" pour la tâche que vous voulez exécuter.
    """
    task = run_long_task.delay()
    return HttpResponse('', status=200)
```

Pour exécuter la tâche il suffit de lancer Django et Celery dans des processus différents.

**Pour Django**
```bash
> python3 manage.py runserver
Performing system checks...

System check identified no issues (0 silenced).
February 11, 2019 - 02:58:13
Django version 2.1.5, using settings 'meetup.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

**Pour Celery**
```bash
> celery -A meetup worker -l info -c 1

++++++ INITIALISATION DE LA TÂCHE
celery@ordi.home v4.2.1 (windowlicker)

Darwin-18.0.0-x86_64-i386-64bit 2019-02-11 02:59:07

[config]
.> app:         meetup:0x10b500b38
.> transport:   amqp://guest:**@localhost:5672//
.> results:     rpc://
.> concurrency: 1 (prefork)
.> task events: OFF (enable -E to monitor tasks in this worker)

[queues]
.> celery           exchange=celery(direct) key=celery

[tasks]
  . meetup.celery.debug_task
  . meetup.tasks.get_band_details_task
  . meetup.tasks.run_long_task
  . meetup.tasks.run_retry_task
  . meetup.tasks.run_time_limits_task
  . meetup.tasks.save_artist
  . meetup.tasks.search_artist
```

Il suffit maintenant de lancer une requête à l'URL /longRunningTask.

**Requête via CURL** 
```
> curl -X POST http://localhost:8000/longRunningTask/
```

Côté Django, vous devez voir la requête arriver et voir la réponse partir rapidement - sans devoir attendre que la tâche soit terminée.

**Django**
```bash
[11/Feb/2019 03:05:12] "POST /longRunningTask HTTP/1.1" 200 0
```

Côté Celery vous verrez la tâche en exécution :

**Celery**
```bash
[2019-02-11 03:05:12,023: INFO/MainProcess] Received task: meetup.tasks.run_long_task[c911cf72-5f68-4271-9795-04738b09af98]
[2019-02-11 03:05:12,025: WARNING/ForkPoolWorker-1] >>>>> DÉBUT
[2019-02-11 03:05:13,026: WARNING/ForkPoolWorker-1] >>>>> FIN
[2019-02-11 03:05:13,049: INFO/ForkPoolWorker-1] Task meetup.tasks.run_long_task[c911cf72-5f68-4271-9795-04738b09af98] succeeded in 1.0249147209979128s: None
```

Vous pouvez aussi lancer le test déclaré dans ```test.py``` avec la commande suivante :

```bash
> python3 manage.py test
System check identified no issues (0 silenced).
.
----------------------------------------------------------------------
Ran 1 test in 1.019s

OK
```

<a name="diapositives"/>

## Diapositives

La présentation se trouve dans le fichier ```slides.pdf``` dans la racine de ce repo.
