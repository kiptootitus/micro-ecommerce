from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from rest_framework import generics, permissions, status, views
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from . import models, serializers


# Create your views here.

class AddressListView(LoginRequiredMixin, generics.ListCreateAPIView):
    queryset = models.Address.objects.all()
    serializer_class = serializers.AddressSerializer
    permission_classes = [permissions.IsAuthenticated]


class AddressDetailView(LoginRequiredMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Address.objects.all()
    serializer_class = serializers.AddressSerializer
    permission_classes = [permissions.IsAuthenticated]


class ContactListView(LoginRequiredMixin, generics.ListCreateAPIView):
    queryset = models.Contact.objects.all()
    serializer_class = serializers.ContactSerializer
    permission_classes = [permissions.IsAuthenticated]


class CreateProfileView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """Render a form page for profile creation (if needed)"""
        return render(request, 'profile_create.html')

    def post(self, request, *args, **kwargs):
        """Handle profile creation"""
        data = request.data.copy()  # Copy to avoid modifying original data
        data['user'] = request.user.id
        serializer = serializers.ProfileSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ProfileListView(LoginRequiredMixin, generics.ListCreateAPIView):
    queryset = models.Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProfileDetailView(LoginRequiredMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
