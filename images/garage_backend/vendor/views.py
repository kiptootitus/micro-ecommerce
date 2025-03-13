from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import permissions, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Vendor
from .serializers import VendorSerializer


# Register a new Vendor
class RegisterVendorView(generics.CreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [permissions.AllowAny]  # Anyone can register

    def perform_create(self, serializer):
        # Ensure that 'created_by' exists in Vendor model before using
        serializer.save()


# Login View (Should ideally be handled via Django authentication, not here)
class LoginVendorView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        return Response({"message": "Implement login logic here"})


# List Vendors (Login required)
@method_decorator(cache_page(60 * 15), name='dispatch')
class VendorListView(generics.ListAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [permissions.IsAuthenticated]


# Retrieve, Update, Delete Vendor (Login required)
@method_decorator(cache_page(60 * 15), name='dispatch')
class VendorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [permissions.IsAuthenticated]
