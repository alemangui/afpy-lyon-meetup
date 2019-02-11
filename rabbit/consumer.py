import pika

# D'abord il faut se connecter au serveur RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1'))
channel = connection.channel()

# On va s'assurer que la queue existe
channel.queue_declare(queue='python-meetup')

# On crée la function a appeller lors qu'un message est reçu
def callback(channel, method, properties, body):
    print('On a reçu ce message: {0} (^_^)'.format(body))

# Et on dit à Pika de l'appeller quand on aura un message
channel.basic_consume(callback, queue='python-meetup', no_ack=True)

# On va se mettre en boucle infini en attendant les messages
print('On attend des messages {-_-}')
channel.start_consuming()
