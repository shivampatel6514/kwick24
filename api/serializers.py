from rest_framework import serializers
from .models import User, Category, Subcategory, Service, Address

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name', 'email', 'phone',
            'role', 'is_verified'
        ]
class SubcategorySerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)  # Include image field

    class Meta:
        model = Subcategory
        fields = ['id', 'name', 'image', 'created_at', 'updated_at']

class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubcategorySerializer(many=True, read_only=True, source='subcategory_set')  # Nested subcategories
    image = serializers.ImageField(required=False)  # Include image field

    class Meta:
        model = Category
        fields = ['id', 'name', 'image','adds_image','adds_title','adds_description','adds_status' ,'subcategories', 'created_at', 'updated_at']


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name', 'user', 'category', 'subcategory', 'location', 'availability', 'created_at', 'updated_at']


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'user', 'city', 'pincode', 'state', 'street', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    # Ensure user is passed in context or validated
    def validate_user(self, value):
        if self.context['request'].user != value:
            raise serializers.ValidationError("You can only create or update your own addresses.")
        return value