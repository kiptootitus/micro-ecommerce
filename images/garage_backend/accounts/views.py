from allauth.account.views import SignupView, LoginView, LogoutView
from django.urls import reverse_lazy
from rest_framework import generics, permissions

from .models import Users
from .serializers import UserSerializer


# API Views
class UserListCreateView(generics.ListCreateAPIView):
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]  # Only admins can list/create

    def perform_create(self, serializer):
        # Custom logic before saving
        serializer.save()


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Allow users to only access their own data unless admin
        obj = super().get_object()
        if not self.request.user.is_administrator and obj != self.request.user:
            self.permission_denied(self.request)
        return obj


# Allauth Views (optional customization)
class CustomSignupView(SignupView):
    template_name = 'account/custom_signup.html'
    success_url = reverse_lazy('home')


class CustomLoginView(LoginView):
    template_name = 'account/custom_login.html'

    def form_valid(self, form):
        print("You are being directed to the home page")
        return super().form_valid(form)



class CustomLogoutView(LogoutView):
    template_name = 'account/custom_logout.html'
