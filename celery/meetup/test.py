import builtins
from unittest import mock
from django.test import SimpleTestCase, Client, override_settings
from django.urls import reverse


class TestMeetup(SimpleTestCase):
    """
    TestMeetup hérite de SimpleTestCase au lieu de TestCase
    car on n'a pas de base de données pour ce projet.
    """

    @mock.patch('builtins.print')
    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_print_called(self, mocked_print):
        """
        Notre tâche imprime ">>>>> DÉBUT" au commencement de l'exécution et
        ">>>>> FIN" quand elle a fini. Ce test vérifie que ces deux chaînes
        de caractères sont bien imprimées quand on appelle l'URL
        "/longRunningTask". Pour cela, on crée un mock de "print" et on
        regarde avec quels paramètres la fonction a été appelée.

        Vu que les tâches sont exécutées par un processus différent (Celery
        et non pas Django), on soit surcharger le paramètre
        CELERY_TASK_ALWAYS_EAGER du settings.py qui permet le processus du
        test Django de prendre directement en charge les tâches sans passer
        par Celery.
        """
        Client().post(reverse('task_view'), format='json')

        printed_args = map(lambda x: x[0][0], mocked_print.call_args_list)

        self.assertIn('>>>>> DÉBUT', printed_args)
        self.assertIn('>>>>> FIN', printed_args)
