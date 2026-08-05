# Real-Time Notification & Webhook Engine

An enterprise-grade Django microservice for event-driven real-time notifications and external webhook dispatch.

## Local Setup

1. Configure a local PostgreSQL database named `notification_db`.
2. Ensure your `.env` file matches the PostgreSQL credentials.
3. Install dependencies:
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
4. Run migrations:
   python manage.py migrate
5. Start the server:
   python manage.py runserver

## Architecture
- Web Framework: Django
- Database: PostgreSQL
- Real-Time: Django Channels & Redis
- Background Tasks: Celery