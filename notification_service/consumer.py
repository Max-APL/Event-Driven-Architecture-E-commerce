import json
from rabbitmq_utils import create_consumer
from notification_service.mailer import send_notification

def handle_payment_processed(ch, method, properties, body):
    data = json.loads(body)
    print(f"📧 NotificationService recibió PaymentProcessed: {data}")
    send_notification(data)

if __name__ == "__main__":
    create_consumer("payment_processed", handle_payment_processed)
