# 🛍️ Event-Driven E-commerce System

Este proyecto implementa una arquitectura de e-commerce basada en microservicios y comunicación orientada a eventos, utilizando RabbitMQ como middleware de mensajería y FastAPI como framework web.

---

## 🚀 Flujo de la Orden de Compra

### 📥 Paso a paso:

**POST /checkout**  
El cliente envía una solicitud de orden con `user_id` y productos.  
🔁 Se emite el evento `OrderRequested`.

- **user_service**  
  Escucha `OrderRequested`, valida el usuario, y responde con:  
  ✅ `UserValidated`

- **inventory_service**  
  Escucha `OrderRequested`, verifica y actualiza stock, luego responde con:  
  ✅ `InventoryUpdated`

- **order_service.event_buffer**  
  Espera ambos eventos (`UserValidated` + `InventoryUpdated`)  
  🟢 Una vez ambos están disponibles, emite: `OrderCreated`

- **payment_service**  
  Escucha `OrderCreated`, simula el pago, y responde con:  
  ✅ `PaymentProcessed`

- **notification_service**  
  Escucha `PaymentProcessed`, y simula el envío de email/notificación.

---

## 🔁 Flujo completo de eventos

```
[POST /checkout]
        ↓
 OrderRequested
   ↙         ↘
UserService  InventoryService
   ↓             ↓
UserValidated  InventoryUpdated
         ↘     ↙
       EventBuffer
           ↓
     OrderCreated
           ↓
    PaymentService
           ↓
   PaymentProcessed
           ↓
 NotificationService
           ↓
Notificación enviada
```

---

## 🧱 Estructura del proyecto

```
ecommerce/
├── rabbitmq_utils.py
├── main.py                        # Punto de entrada FastAPI
├── user_service/
│   ├── consumer.py
│   └── logic.py
├── product_service/
│   └── consumer.py
├── inventory_service/
│   ├── consumer.py
│   └── logic.py
├── order_service/
│   ├── event_buffer.py
│   └── publisher.py
├── payment_service/
│   ├── consumer.py
│   └── logic.py
├── notification_service/
│   ├── consumer.py
│   └── mailer.py
└── shared/
    └── models.py
```

---

## 🛠️ Cómo ejecutar

1. Asegúrate de tener RabbitMQ corriendo localmente:

```
docker run -d -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```

2. Ejecuta FastAPI:

```
uvicorn main:app --reload
```

3. En ventanas de terminal separadas, ejecuta:

```
python -m user_service.consumer
python -m inventory_service.consumer
python -m order_service.event_buffer
python -m payment_service.consumer
python -m notification_service.consumer
```

4. Envía una orden desde Postman o archivo `.http`:

```
POST http://localhost:8000/checkout
Content-Type: application/json

{
  "user_id": "U123",
  "items": [
    { "product_id": "P1", "quantity": 2 },
    { "product_id": "P2", "quantity": 1 }
  ]
}
```

---

## 📡 Tecnologías utilizadas

- Python 3.11+
- FastAPI
- Pika (RabbitMQ client)
- RabbitMQ (mensajería AMQP)
- Uvicorn (servidor ASGI)

---

## 📚 Conceptos aplicados

- Arquitectura orientada a eventos (EDA)
- Microservicios desacoplados
- Comunicación asíncrona con RabbitMQ
- Coordinación de eventos con buffers
- Servicios independientes por dominio

---

## 🔄 Flujo Detallado por Servicios

### 🧾 1. Cliente — FastAPI (`main.py`)

**Ruta:** `POST /checkout`  
**Acción:**
- Genera `order_id` único.
- Publica evento `OrderRequested`.

**Mensaje en consola:**
```json
{
  "message": "Orden solicitada",
  "order_id": "f3d949cf-e773-424c-9493-38a19ab64b1b"
}
```

📤 **Evento emitido:**
```json
{
  "type": "OrderRequested",
  "order_id": "...",
  "user_id": "U123",
  "items": [...]
}
```

---

### 👤 2. `user_service/consumer.py`

**Escucha:** `OrderRequested`  
**Acción:**
- Valida si el `user_id` comienza con "U".
- Publica `UserValidated` si es válido.

**Mensajes en consola:**
```
👤 UserService recibió OrderRequested: {...}
✅ Usuario U123 validado, evento enviado
```

📤 **Evento emitido:**
```json
{
  "type": "UserValidated",
  "order_id": "...",
  "user_id": "U123"
}
```

---

### 📦 3. `inventory_service/consumer.py`

**Escucha:** `OrderRequested`  
**Acción:**
- Verifica si hay stock suficiente para cada `product_id`.
- Si lo hay, descuenta del stock y emite `InventoryUpdated`.

**Mensajes en consola:**
```
📦 InventoryService recibió OrderRequested: {...}
✅ Inventario actualizado para orden f3d949cf...
```

📤 **Evento emitido:**
```json
{
  "type": "InventoryUpdated",
  "order_id": "..."
}
```

---

### ⚙️ 4. `order_service/event_buffer.py`

**Escucha:**  
- `UserValidated`  
- `InventoryUpdated`

**Acción:**
- Guarda en buffers temporales.
- Cuando ambos eventos coinciden por `order_id`, emite `OrderCreated`.

**Mensajes en consola:**
```
📦 OrderService recibió InventoryUpdated: {...}
👤 OrderService recibió UserValidated: {...}
🟢 OrderCreated emitido para f3d949cf...
```

📤 **Evento emitido:**
```json
{
  "type": "OrderCreated",
  "order_id": "..."
}
```

---

### 💳 5. `payment_service/consumer.py`

**Escucha:** `OrderCreated`  
**Acción:**
- Simula un cobro (siempre exitoso por ahora).
- Emite `PaymentProcessed`.

**Mensajes en consola:**
```
💳 PaymentService recibió OrderCreated: {...}
💸 Procesando pago para orden f3d949cf...
✅ Pago procesado para orden f3d949cf...
```

📤 **Evento emitido:**
```json
{
  "type": "PaymentProcessed",
  "order_id": "...",
  "status": "success"
}
```

---

### 📧 6. `notification_service/consumer.py`

**Escucha:** `PaymentProcessed`  
**Acción:**
- Simula el envío de un email de confirmación.

**Mensajes en consola:**
```
📧 NotificationService recibió PaymentProcessed: {...}
📨 Notificación enviada: Tu orden f3d949cf... fue pagada con éxito.
```

📤 **Sin eventos nuevos emitidos (fin del flujo)**

---

## 🔚 Resultado final

> El sistema ha recibido una orden, verificado usuario y stock, generado la orden, cobrado y notificado al usuario, todo mediante eventos independientes, sin acoplamiento directo entre servicios.
