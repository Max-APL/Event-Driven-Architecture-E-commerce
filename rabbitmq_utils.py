import pika
import json

RABBITMQ_HOST = "localhost"
RABBITMQ_USER = "manager"
RABBITMQ_PASS = "1590rabbit"

def get_connection():
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    parameters = pika.ConnectionParameters(RABBITMQ_HOST, credentials=credentials)
    return pika.BlockingConnection(parameters)

def publish_event(exchange: str, event: dict):
    connection = get_connection()
    channel = connection.channel()
    channel.exchange_declare(exchange=exchange, exchange_type="fanout")
    channel.basic_publish(exchange=exchange, routing_key="", body=json.dumps(event))
    connection.close()

def create_consumer(exchange: str, callback):
    connection = get_connection()
    channel = connection.channel()
    channel.exchange_declare(exchange=exchange, exchange_type="fanout")
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange=exchange, queue=queue_name)
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    print(f"🎧 Escuchando en exchange '{exchange}'...")
    channel.start_consuming()
