def send_notification(payment_event):
    order_id = payment_event["order_id"]
    print(f"📨 Notificación enviada: Tu orden {order_id} fue pagada con éxito.")
