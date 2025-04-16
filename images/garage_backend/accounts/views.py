from allauth.account.views import SignupView, LoginView, LogoutView
from django.urls import reverse_lazy
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Users, Profile
from .serializers import UserSerializer, UserLoginSerializer, ProfileSerializer
from rest_framework.permissions import IsAuthenticated

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


class UserRegisterCreateView(generics.CreateAPIView):
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                'message': 'User registered successfully',
                'user_id': serializer.instance.user_id
            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user = Users.objects.get(email=email)
            if user.check_password(password):
                return Response(
                    {
                        'message': 'Login successful',
                        'user_id': user.user_id
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'message': 'Invalid credentials'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Users.DoesNotExist:
            return Response(
                {'message': 'User does not exist'},
                status=status.HTTP_404_NOT_FOUND
            )


class ProfileCreateView(generics.CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]


class UserProfileDetailView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

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
