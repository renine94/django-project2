import random

from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from accounts.models import User, PhoneAuthentication
from accounts.serializers import AccountSerializer


# Create your views here.
class AccountAPI(mixins.CreateModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['get'], url_path='confirm-code')
    def confirm_code(self, request):
        """회원가입 전 전화번호 인증 문자 발송"""
        phone_number = request.query_params.get('phone_number')
        confirm_cde = ''.join([str(random.choice(range(10))) for _ in range(6)])

        # TODO 실제 외부모듈 연결후 SMS 전송
        pass

        PhoneAuthentication.objects.create(
            phone_number=phone_number,
            confirm_code=confirm_cde
        )

        return Response({'message': f'인증번호 [] 발송되었습니다.'}, status=status.HTTP_200_OK)

    @confirm_code.mapping.post
    def confirm_code_check(self, request):
        """회원가입 인증 문자 체크, 없으면 404"""
        phone_number = request.data.get('phone_number')
        confirm_code = request.data.get('confirm_code')
        get_object_or_404(PhoneAuthentication, phone_number=phone_number, confirm_code=confirm_code)
        return Response({'meesage': True}, status=status.HTTP_200_OK)


class LoginAPI():
    pass
