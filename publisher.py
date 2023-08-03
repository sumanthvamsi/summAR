from django.db import models
import pika
import json
class BackendData(models.Model):
    variable = models.CharField(max_length=255)



# RabbitMQ connection parameters
RABBITMQ_HOST = 'localhost'
RABBITMQ_PORT = 5672
RABBITMQ_USERNAME = 'guest'
RABBITMQ_PASSWORD = 'guest'

# Callback function to handle incoming messages
def handle_message(channel, method, properties, body):
    # Decode the message body as JSON
    message = json.loads(body)

    update_backend_value(message)
        
    # Acknowledge the message
    channel.basic_ack(delivery_tag=method.delivery_tag)


def update_backend_value(data):
# Retrieve or create the BackendData instance
    backend_data, created = BackendData.objects.get_or_create(pk=1)
# Update the value
    backend_data.variable = data
    backend_data.save()


# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host=RABBITMQ_HOST,
    port=RABBITMQ_PORT,
    credentials=pika.PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD)
))
channel = connection.channel()

# Declare the exchange
channel.exchange_declare(exchange='smart_meter', exchange_type='fanout')

# Declare a queue with a random name
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

# Bind the queue to the exchange
channel.queue_bind(exchange='smart_meter', queue=queue_name)

# Set the callback function for incoming messages
channel.basic_consume(queue=queue_name, on_message_callback=handle_message)

# Start consuming messages
channel.start_consuming()