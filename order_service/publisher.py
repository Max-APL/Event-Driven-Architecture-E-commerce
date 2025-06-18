from rabbitmq_utils import publish_event

def publish_order_requested(event: dict):
    publish_event("order_requested", event)
