This folder is a lightweight duplicate placeholder for the alx_travel_app_0x03 submission.

The full project is available at the repository root. For the Celery + RabbitMQ exercise, review the changes made in the main project:

- alx_travel_app/alx_travel_app/celery.py  -> project Celery app
- alx_travel_app/listings/tasks.py        -> Celery task to send booking confirmation
- alx_travel_app/listings/views.py        -> BookingViewSet triggers the task on create
- alx_travel_app/alx_travel_app/settings.py -> EMAIL and CELERY config

Run instructions (example):

1. Start RabbitMQ (ensure it is running on amqp://guest:guest@localhost:5672/)
2. Start Django: `python manage.py runserver`
3. Start Celery worker: `celery -A alx_travel_app worker --loglevel=info`
4. Create a booking via POST to `/api/bookings/` to trigger an async email (console backend by default).