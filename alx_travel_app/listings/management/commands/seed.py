from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from listings.models import Listing, Booking, Review
from datetime import date, timedelta
import random

class Command(BaseCommand):
    help = 'Seed the database with sample travel app data'

    def handle(self, *args, **options):
        # Create sample users if they don't exist
        users_data = [
            {'username': 'john_doe', 'email': 'john@example.com'},
            {'username': 'jane_smith', 'email': 'jane@example.com'},
            {'username': 'admin_user', 'email': 'admin@example.com'},
        ]
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={'email': user_data['email']}
            )
            if created:
                user.set_password('password123')  # Set a default password
                user.save()
                self.stdout.write(self.style.SUCCESS(f'Created user: {user.username}'))

        # Sample listings data
        listings_data = [
            {
                'title': 'Cozy Beach Apartment',
                'description': 'A relaxing apartment by the sea with ocean views.',
                'property_type': 'apartment',
                'price_per_night': 150.00,
                'location': 'Miami Beach, FL',
                'bedrooms': 2,
                'bathrooms': 1,
                'guests': 4,
                'amenities': ['wifi', 'pool', 'beach_access'],
                'image': 'https://example.com/beach-apartment.jpg',
                'owner': User.objects.get(username='john_doe'),
            },
            {
                'title': 'Luxury Mountain Villa',
                'description': 'Spacious villa in the Rockies with hot tub.',
                'property_type': 'villa',
                'price_per_night': 350.00,
                'location': 'Aspen, CO',
                'bedrooms': 4,
                'bathrooms': 3,
                'guests': 8,
                'amenities': ['fireplace', 'hot_tub', 'ski_access'],
                'image': 'https://example.com/mountain-villa.jpg',
                'owner': User.objects.get(username='jane_smith'),
            },
            {
                'title': 'Downtown Hotel Suite',
                'description': 'Modern suite in the heart of the city.',
                'property_type': 'hotel',
                'price_per_night': 200.00,
                'location': 'New York, NY',
                'bedrooms': 1,
                'bathrooms': 1,
                'guests': 2,
                'amenities': ['gym', 'spa', 'concierge'],
                'image': 'https://example.com/hotel-suite.jpg',
                'owner': User.objects.get(username='admin_user'),
            },
        ]

        # Create listings
        created_listings = []
        for data in listings_data:
            listing, created = Listing.objects.get_or_create(
                title=data['title'],
                defaults={k: v for k, v in data.items() if k != 'owner'}
            )
            if created:
                listing.owner = data['owner']
                listing.save()
                created_listings.append(listing)
                self.stdout.write(self.style.SUCCESS(f'Created listing: {listing.title}'))

        # Create sample bookings (only if listings exist)
        if created_listings:
            booking_data = []
            for _ in range(5):  # Create 5 sample bookings
                listing = random.choice(created_listings)
                user = random.choice(User.objects.all())
                check_in = date.today() + timedelta(days=random.randint(1, 30))
                check_out = check_in + timedelta(days=random.randint(1, 7))
                total_price = listing.price_per_night * (check_out - check_in).days
                booking_data.append({
                    'listing': listing,
                    'user': user,
                    'check_in_date': check_in,
                    'check_out_date': check_out,
                    'total_price': total_price,
                    'status': random.choice(['pending', 'confirmed', 'cancelled']),
                })
            
            for data in booking_data:
                Booking.objects.create(**data)
                self.stdout.write(self.style.SUCCESS(f'Created booking for {data["listing"].title}'))

        # Create sample reviews (only if listings exist)
        if created_listings:
            for listing in created_listings:
                for _ in range(random.randint(1, 3)):  # 1-3 reviews per listing
                    user = random.choice(User.objects.all())
                    Review.objects.create(
                        listing=listing,
                        user=user,
                        rating=random.randint(1, 5),
                        comment=f"Sample review for {listing.title} - Great stay!"
                    )
                    self.stdout.write(self.style.SUCCESS(f'Created review for {listing.title}'))

        self.stdout.write(self.style.SUCCESS('Database seeding completed successfully!'))