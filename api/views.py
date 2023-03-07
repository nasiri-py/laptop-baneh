from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, ProductSerializer
from rest_framework import viewsets
from rest_framework.views import APIView
from accounts.models import User
from products.models import Product
from rest_framework.permissions import IsAdminUser, IsAuthenticated


class UserViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = UserSerializer

    def list(self, request):
        """
            List of users
        """

        user = User.objects.all()
        ser_data = UserSerializer(user, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)

    def create(self, request):
        """
            Create a new user
        """

        ser_data = UserSerializer(data=request.POST)
        if ser_data.is_valid():
            ser_data.create(ser_data.validated_data)
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(data=ser_data.errors, status=status.HTTP_403_FORBIDDEN)

    def retrieve(self, request, pk=None):
        """
            User detail
        """

        user = get_object_or_404(User, pk=pk)
        ser_data = UserSerializer(user)
        return Response(ser_data.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        """
            Update a user
        """

        user = get_object_or_404(User, pk=pk)
        if not request.user.is_superuser or user != request.user:
            return Response({'permission denied': 'you are not superuser or owner'})
        ser_data = UserSerializer(instance=user, data=request.POST, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(data=ser_data.errors, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, pk=None):
        """
            Deactive a user
        """
        user = get_object_or_404(User, pk=pk)
        if not request.user.is_superuser or user != request.user:
            return Response({'permission denied': 'you are not superuser or owner'})
        user.is_active = False
        user.save()
        return Response({'message': 'user deactivated'})


class ProductApiListView(APIView):
    serializer_class = ProductSerializer

    def get(self, request):
        """
            List of products
        """
        products = Product.objects.all()
        ser_data = ProductSerializer(products, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)


class ProductApiDetailView(APIView):
    serializer_class = ProductSerializer

    def get(self, request, pk):
        """
            Product detail
        """
        product = get_object_or_404(Product, pk=pk)
        ser_data = ProductSerializer(product)
        return Response(ser_data.data, status=status.HTTP_200_OK)


class ProductApiDeleteView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = ProductSerializer

    def delete(self, request, pk):
        """
            Delete a products
        """

        product = get_object_or_404(Product, pk=pk)
        self.check_object_permissions(request, product)
        product.delete()
        return Response({'message': 'product deleted'})
