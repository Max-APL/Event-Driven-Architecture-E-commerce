from fastapi import FastAPI
from order_service.publisher import publish_order_requested
from shared.models import OrderRequest
import uuid

app = FastAPI()

@app.post("/checkout")
def checkout(order: OrderRequest):
    order_id = str(uuid.uuid4())
    event = {
        "type": "OrderRequested",
        "order_id": order_id,
        "user_id": order.user_id,
        "items": [item.dict() for item in order.items]
    }
    publish_order_requested(event)
    return {"message": "Orden solicitada", "order_id": order_id}
