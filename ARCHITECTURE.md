# Real-Time Notification & Webhook Engine

## 1. System Objective
A centralized microservice responsible for receiving internal system events, persisting them, broadcasting them in real-time to connected WebSocket clients, and dispatching them asynchronously to registered external webhook URLs with guaranteed delivery mechanisms.

## 2. Core Components

### 2.1 API Layer (Django REST Framework)
- JWT-secured endpoints for client authentication.
- Endpoints to register, update, and delete third-party Webhook subscription URLs.
- Internal ingestion endpoint to receive events from other internal microservices.

### 2.2 Real-Time Layer (Django Channels)
- ASGI application handling WebSocket connections.
- Redis-backed channel layers for broadcasting events to specific user groups or global channels.

### 2.3 Asynchronous Worker Layer (Celery)
- Dedicated worker pool for webhook dispatch.
- Implementation of exponential backoff for failed webhook deliveries.
- Dead-letter queue mechanism for permanently failed payloads.

### 2.4 Persistence Layer (PostgreSQL)
- Strict relational schema for Users, Notifications, WebhookSubscriptions, and WebhookDeliveryLogs.
- Indexed fields for fast querying of delivery statuses.

## 3. Security Perimeter
- All endpoints strictly enforce Role-Based Access Control (RBAC).
- WebSocket connections require JWT validation during the handshake phase.
- Webhook payloads are signed using HMAC SHA-256 to allow third-party verification.
- Database interactions utilize Django's ORM to prevent SQL injection.