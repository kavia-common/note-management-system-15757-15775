from rest_framework import status, generics, permissions, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import login, logout
from rest_framework.authtoken.models import Token
from .serializers import (
    RegisterSerializer, LoginSerializer, UserSerializer, NoteSerializer
)
from .models import Note

# PUBLIC_INTERFACE
@api_view(['GET'])
def health(request):
    """
    Health check endpoint.
    Returns 200 if the server is up.
    ---
    responses:
        200:
            description: Success message.
    """
    return Response({"message": "Server is up!"})

# PUBLIC_INTERFACE
class RegisterView(generics.CreateAPIView):
    """
    Registers a new user in the system.
    """
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

# PUBLIC_INTERFACE
class LoginView(APIView):
    """
    Authenticates a user and returns a token.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "token": token.key,
                "user": UserSerializer(user).data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# PUBLIC_INTERFACE
class LogoutView(APIView):
    """
    Logs out the current user.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()
        except Exception:
            pass
        logout(request)
        return Response({"message": "Logged out successfully."}, status=status.HTTP_200_OK)

# PUBLIC_INTERFACE
class UserView(generics.RetrieveAPIView):
    """
    Retrieves the current authenticated user's information.
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

# PUBLIC_INTERFACE
class NoteViewSet(viewsets.ModelViewSet):
    """
    API endpoint for CRUD operations on Notes.
    """
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user).order_by('-updated_at')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
