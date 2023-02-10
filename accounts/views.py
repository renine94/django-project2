from django.http import JsonResponse
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from accounts.models import User
from accounts.serializers import AccountSerializer


# Create your views here.
class AccountAPI(mixins.CreateModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [AllowAny]

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @action(detail=False, methods=['get'])
    def send_confirm_code(self, request):
        """전화번호 인증 문자 발송"""
        user = self.get_object()

        return Response({'message': f'인증번호 [] 발송되었습니다.'}, status=status.HTTP_200_OK)
