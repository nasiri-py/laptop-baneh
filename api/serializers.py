from rest_framework import serializers
from accounts.models import User
from products.models import Product


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        return User.objects.create_user(
            phone_number=validated_data['phone_number'],
            username=validated_data['username'],
            password=validated_data['password']
        )


class ProductSerializer(serializers.ModelSerializer):
    brand = serializers.StringRelatedField()
    category = serializers.StringRelatedField(many=True)

    class Meta:
        model = Product
        fields = '__all__'
