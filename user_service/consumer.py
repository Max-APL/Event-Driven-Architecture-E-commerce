import json
from rabbitmq_utils import create_consumer, publish_event
from user_service.logic import validate_user

def handle_order_requested(ch, method, properties, body):
    event = json.loads(body)
    print(f"👤 UserService recibió OrderRequested: {event}")
    user_id = event.get("user_id")

    if validate_user(user_id):
        response = {
            "type": "UserValidated",
            "user_id": user_id,
            "order_id": event["order_id"]
        }
        publish_event("user_validated", response)
        print(f"✅ Usuario {user_id} validado, evento enviado")
    else:
        print(f"❌ Usuario {user_id} inválido")

if __name__ == "__main__":
    create_consumer("order_requested", handle_order_requested)
