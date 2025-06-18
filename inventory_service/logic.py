# Simula control de stock local
STOCK = {
    "P1": 10,
    "P2": 5,
    "P3": 8
}

def check_and_update_inventory(items: list[dict]) -> bool:
    # Verifica si hay stock suficiente
    for item in items:
        product_id = item["product_id"]
        qty = item["quantity"]
        if STOCK.get(product_id, 0) < qty:
            return False  # stock insuficiente

    # Si hay stock, se descuenta
    for item in items:
        product_id = item["product_id"]
        qty = item["quantity"]
        STOCK[product_id] -= qty

    return True
