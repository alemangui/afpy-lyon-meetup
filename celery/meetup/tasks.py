import time
from celery import shared_task, Task
from celery.exceptions import SoftTimeLimitExceeded


class MeetupTask(Task):
    """
    On peut créer des sous-classes de Task. Ceci nous permet
    d'ajouter de la fonctionnalité et de partager des ressources
    entre tâches.
    """
    def __init__(self):
        """
        Notez que __init__ n'est appellé qu'une seule fois.
        """
        print('++++++ INITIALISATION DE LA TÂCHE')
        self.db_connector = 'Je suis le connecteur partagé'


@shared_task(bind=True, base=MeetupTask)
def run_long_task(self):
    """
    Une tâche simple qu'attend une seconde.

    En utilisant "bind=True" comme paramètre dans
    le décorateur "@shared_task", le paramètre "self"
    sera assigné à l'instance Task en question.

    Notez que cette tâche est une instance de "MeetupTask"
    qu'on a déclaré plus haut. Ceci à cause du
    "base=MeetupTask" qu'on a mis comme paramètre
    dans le décorateur "@shared_task"
    """
    print('>>>>> DÉBUT')
    time.sleep(1)
    print('>>>>> FIN')


@shared_task(autoretry_for=(Exception, ), retry_kwargs={'max_retries': 5}, default_retry_delay=1)
def run_retry_task():
    """
    Cette tâche n'aboutira jamais, car on lève une exception au milieu.

    Celery va ressayer l'exécution de la tâche automatiquement si
    elle lance une exception de type "Exception". On arrive à le faire
    en mettant "autoretry_for=(Exception, )" dans les paramètres du décorateur.

    La tâche va échouer les tentatives subséquentes aussi. Pour éviter
    une boucle infinie, on demande à Celery de ne pas ressayer plus de
    cinq fois - d'où le "retry_kwargs={'max_retries': 5}" présent aussi
    dans les paramètres du décorateur.

    Finalement, on a aussi choisi le délai entre chaque tentative. Dans cet
    exemple ce délai est d'une seconde : default_retry_delay=1.
    """
    print('>>>>> DÉBUT')
    time.sleep(1)
    raise Exception
    print('>>>>> FIN') # Cette ligne ne sera jamais atteinte


@shared_task(soft_time_limit=3)
def run_time_limits_task():
    """
    Cette tâche prendra cinq secondes pour finir,
    mais on a mis en place une limitation à trois secondes.

    Vu que cette limitation est en forme de soft_time_limit
    (et non pas time_limit), on peut attraper l'exception levé
    suite au dépassement du temps autorisé (SoftTimeLimitExceeded)
    et éventuellement faire des actions additionnelles. Ceci ne
    serait pas possible en ayant un time_limit tout court.
    """
    try:
        print('>>>>> DÉBUT')
        time.sleep(5)
        print('>>>>> FIN')
    except SoftTimeLimitExceeded as _:
        print('>>>>> TIME LIMIT EXCEPTION CAUGHT')

"""
=====================
CHAINS
=====================

Les tâches Celery peuvent aussi d'enchaîner les unes après les
autres dans un ordre donné. Cette fonctionnalité nous permet de
créer des dépendances entre des tâches, pour s'assurer que l'ordre
d'exécution soit correct et passer les valeurs de retour d'une tâche
comme paramètre de la suivante. Celery appelle ça les "chains".

Les fonctions ci-desous simulent une action pour récupérer et
sauvegarder en base les données d'un artiste. La première tâche
simule la recherche dans une API le nom de l'artiste. La deuxième
récupère les informations du premier résultat de la recherche précédente.
La troisième tâche sauvegarde ces données en base. Les appels réseau et
la sauvegarde en base ont été remplacés par des time.sleep.

Finalement, la fonction scrape_artist_data va créer la "chain" de
ces trois tâches et démarrera leur exécution.
"""


@shared_task
def search_artist(artist_name):
    """
    Cette tâche simule un appel à une API pour chercher un artiste par
    son nom. Le retour sera une liste de résultats comprenant le nom de
    l'artiste et son ID. Pour simuler le temps d'attente de l'appel
    réseau on utilisera un time.sleep.
    """
    print('Searching for {0}'.format(artist_name))
    time.sleep(1) # On dit que l'appel API a pris une seconde
    return (
        ('Pink Floyd', 'c00aabe8-52d0-4437-a450-7b16a2596bcb'),
        ('Pink Floyd Tribute Band', 'ed376471-0e77-4ebc-ae0e-332247f2eb1f'),
        ('The Australian Pink Floyd Show', 'c47737c7-1cd1-44ae-a8b9-e86020346407'),
    )


@shared_task
def get_band_details_task(artist_search_results):
    """
    Cette tâche reçoit comme paramètre les résultats de la recherche de
    la tâche précédente et obtient les informations du premier résultat.
    Pour simuler le temps d'attente de l'appel réseau on utilisera un
    time.sleep.
    """
    print('Getting info for artist {0}'.format(artist_search_results[0]))
    time.sleep(2) # On dit que l'appel API a pris deux secondes
    return {
        'name': 'Pink Floyd',
        'id': 'c00aabe8-52d0-4437-a450-7b16a2596bcb',
        'creation': 1965,
        'members': [
            'Nick Mason',
            'Roger Waters',
            'Richard Wright',
            'Syd Barrett',
            'David Gilmour',
        ]
    }


@shared_task
def save_artist(artist):
    """
    Cette tâche sauvegarde en base de données l'information de l'artiste qu'on
    a obtenu dans la tâche précédente. Pour simuler un temps de sauvegarde (très
    lent) on utilisera un time.sleep.
    """
    print('Saving artist {0}'.format(artist.get('name')))
    time.sleep(1) # On dit que la sauvegarde en base a pris 1 seconde
    return True


def scrape_artist_data(artist_name='Pink Floyd'):
    """
    Finalement, ici on enchaîne les tâches ensemble pour garantir qu'elles seront
    exécutées dans le bon ordre et en passant les paramètres nécessaires à la
    tâche suivante.
    """
    chain = search_artist.s(artist_name) | get_band_details_task.s() | save_artist.s()
    chain.delay()
