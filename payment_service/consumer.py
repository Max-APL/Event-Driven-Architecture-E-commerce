import json
from rabbitmq_utils import create_consumer, publish_event
from payment_service.logic import process_payment

def handle_order_created(ch, method, properties, body):
    data = json.loads(body)
    print(f"💳 PaymentService recibió OrderCreated: {data}")
    order_id = data["order_id"]

    success = process_payment(order_id)
    if success:
        event = {
            "type": "PaymentProcessed",
            "order_id": order_id,
            "status": "success"
        }
        publish_event("payment_processed", event)
        print(f"✅ Pago procesado para orden {order_id}")
    else:
        print(f"❌ Pago fallido para orden {order_id}")

if __name__ == "__main__":
    create_consumer("order_created", handle_order_created)
