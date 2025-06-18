import json
import threading
from collections import defaultdict
from rabbitmq_utils import create_consumer, publish_event

# Buffers para almacenar eventos intermedios
validated_users = set()
updated_inventories = set()

# Usamos un lock para acceso seguro
lock = threading.Lock()

def check_and_emit_order_created(order_id):
    if order_id in validated_users and order_id in updated_inventories:
        event = {
            "type": "OrderCreated",
            "order_id": order_id
        }
        publish_event("order_created", event)
        print(f"🟢 OrderCreated emitido para {order_id}")
        # Limpiamos del buffer
        validated_users.discard(order_id)
        updated_inventories.discard(order_id)

def handle_user_validated(ch, method, properties, body):
    data = json.loads(body)
    print(f"👤 OrderService recibió UserValidated: {data}")
    order_id = data["order_id"]

    with lock:
        validated_users.add(order_id)
        check_and_emit_order_created(order_id)

def handle_inventory_updated(ch, method, properties, body):
    data = json.loads(body)
    print(f"📦 OrderService recibió InventoryUpdated: {data}")
    order_id = data["order_id"]

    with lock:
        updated_inventories.add(order_id)
        check_and_emit_order_created(order_id)

# Iniciar dos consumidores en hilos diferentes
def start_consumers():
    threading.Thread(target=lambda: create_consumer("user_validated", handle_user_validated), daemon=True).start()
    threading.Thread(target=lambda: create_consumer("inventory_updated", handle_inventory_updated), daemon=True).start()
    print("🟠 OrderService esperando UserValidated & InventoryUpdated...")

if __name__ == "__main__":
    start_consumers()
    # Bloquea el hilo principal
    threading.Event().wait()
