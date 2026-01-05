from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Booking


@shared_task
def send_booking_confirmation(booking_id, recipient_email=None):
    try:
        booking = Booking.objects.get(id=booking_id)
    except Booking.DoesNotExist:
        return {'status': 'missing', 'booking_id': booking_id}

    recipient = recipient_email or getattr(settings, 'BOOKING_TEST_EMAIL', None)
    if not recipient:
        return {'status': 'no_recipient', 'booking_id': booking_id}

    subject = f"Booking Confirmation — {booking.listing.title}"
    message = (
        f"Hello {booking.customer_name},\n\n"
        f"Your booking for {booking.listing.title} from {booking.check_in} to {booking.check_out} "
        "has been received and is being processed.\n\nThank you for using ALX Travel."
    )

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [recipient])
    return {'status': 'sent', 'booking_id': booking_id, 'recipient': recipient}
