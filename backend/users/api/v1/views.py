from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action, permission_classes
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

from users.models import History
from .serializers import HistorySerializer, RegistrationSerializer


class HistoryView(GenericViewSet, ListModelMixin, CreateModelMixin):
    serializer_class = HistorySerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return History.objects.filter(user=self.request.user).all()


class UserView(GenericViewSet):
    serializer_class = RegistrationSerializer
    permission_classes = [IsAuthenticated]

    @action(methods=['get'], url_path="is_logged", detail=False)
    def is_login(self, request):
        return Response(status=status.HTTP_200_OK)

    @action(methods=['post'], url_path="signup", detail=False, permission_classes=[AllowAny])
    def registration(self, request: Request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)

