# Simula validación de usuario

def validate_user(user_id: str) -> bool:
    # En un sistema real, harías consultas a DB
    # Aquí simulamos que todo usuario que empieza con "U" es válido
    return user_id.startswith("U")
