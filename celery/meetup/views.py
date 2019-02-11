from django.http import HttpResponse

# Quelques tâches qu'on a défini dans tasks.py
from meetup.tasks import run_long_task
from meetup.tasks import run_retry_task
from meetup.tasks import run_time_limits_task

# La fonction qui crée l'enchaînement des autres tâches.
# Attention, il ne faut pas appeler celle-ci avec .delay
from meetup.tasks import scrape_artist_data

def task_view(request):
    """
    Cette view sera appelée à chaque requête arrivant sur "/longRunningTask".
    Vous pouvez ici remplacer "run_long_task" pour la tâche que vous voulez exécuter.
    """
    task = run_long_task.delay()
    return HttpResponse('', status=200)
