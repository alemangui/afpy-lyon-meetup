import pika

# D'abord il faut se connecter au serveur RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1'))
channel = connection.channel()

# On va s'assurer que la queue existe
channel.queue_declare(queue='python-meetup')

# Maintenant on peut envoyer notre message
for i in range(100):
    channel.basic_publish(exchange='', routing_key='python-meetup', body='Coucou ! {0}'.format(i))
print('Envoyé !')
