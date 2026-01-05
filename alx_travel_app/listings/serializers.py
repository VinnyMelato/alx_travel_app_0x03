from rest_framework import serializers
from .models import Listing, Booking

class ListingSerializer(serializers.ModelSerializer):
    """
    Serializer for Listing model, including nested owner info and review count.
    """
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    average_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Listing
        fields = [
            'id', 'title', 'description', 'property_type', 'price_per_night', 'location',
            'bedrooms', 'bathrooms', 'guests', 'amenities', 'image', 'owner_username',
            'average_rating', 'review_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['owner', 'created_at', 'updated_at']
    
    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews.exists():
            return sum(review.rating for review in reviews) / reviews.count()
        return 0
    
    def get_review_count(self, obj):
        return obj.reviews.count()

class BookingSerializer(serializers.ModelSerializer):
    """
    Serializer for Booking model, including nested listing and user info.
    """
    listing_title = serializers.CharField(source='listing.title', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Booking
        fields = [
            'id', 'listing', 'listing_title', 'user', 'user_username', 'check_in_date',
            'check_out_date', 'total_price', 'status', 'created_at'
        ]
        read_only_fields = ['user', 'created_at']