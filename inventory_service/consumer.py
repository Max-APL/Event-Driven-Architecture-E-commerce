import json
from rabbitmq_utils import create_consumer, publish_event
from inventory_service.logic import check_and_update_inventory

def handle_order_requested(ch, method, properties, body):
    event = json.loads(body)
    print(f"📦 InventoryService recibió OrderRequested: {event}")

    order_id = event.get("order_id")
    items = event.get("items", [])

    if check_and_update_inventory(items):
        response = {
            "type": "InventoryUpdated",
            "order_id": order_id
        }
        publish_event("inventory_updated", response)
        print(f"✅ Inventario actualizado para orden {order_id}")
    else:
        print(f"❌ Stock insuficiente para orden {order_id}")

if __name__ == "__main__":
    create_consumer("order_requested", handle_order_requested)
