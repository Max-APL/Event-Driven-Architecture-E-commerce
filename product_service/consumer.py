import json
from rabbitmq_utils import create_consumer

def handle_order_requested(ch, method, properties, body):
    event = json.loads(body)
    print(f"📦 ProductService recibió OrderRequested: {event}")
    # Aquí solo muestra productos. Podrías agregar validación futura.

if __name__ == "__main__":
    create_consumer("order_requested", handle_order_requested)
