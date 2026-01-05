from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.routers import DefaultRouter

from .models import Booking
from .serializers import BookingSerializer
from .tasks import send_booking_confirmation


def home(request):
    return JsonResponse({"message": "Welcome to ALX Travel API"})


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        booking = serializer.save()

        # Optional: accept `customer_email` in request to send to real customer
        recipient = request.data.get('customer_email')
        send_booking_confirmation.delay(booking.id, recipient)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


router = DefaultRouter()
router.register(r'bookings', BookingViewSet, basename='booking')

