import random

from django.contrib.auth import authenticate
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.models import User, PhoneAuthentication
from accounts.serializers import AccountSerializer, MyTokenObtainPairSerializer, \
    PasswordCheckSerializer


# Create your views here.
class AccountAPI(mixins.CreateModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [AllowAny]

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'retrieve':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    """
    회원가입시 핸드폰 인증
    """
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

        return Response({'message': f'인증번호 [{confirm_cde}] 발송되었습니다.'}, status=status.HTTP_200_OK)

    @confirm_code.mapping.post
    def confirm_code_check(self, request):
        """회원가입 인증 문자 체크, 없으면 404"""
        phone_number = request.data.get('phone_number')
        confirm_code = request.data.get('confirm_code')
        get_object_or_404(PhoneAuthentication, phone_number=phone_number, confirm_code=confirm_code)
        return Response({'meesage': True}, status=status.HTTP_200_OK)

    """
    비밀번호 찾기
    """
    @action(detail=False, methods=['get'], url_path='find-password')
    def find_password(self, request):
        phone_number = request.query_params.get('phone_number')
        if not phone_number:
            return Response({'message': '휴대번호를 입력해주세요.'}, status=status.HTTP_400_BAD_REQUEST)

        confirm_cde = ''.join([str(random.choice(range(10))) for _ in range(6)])

        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            return Response({'message': '해당 번호로 존재하는 아이디가 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

        # TODO SMS 보내기
        pass

        user.confirm_code = confirm_cde
        user.save()
        return Response({'message': f'인증번호 [{confirm_cde}] 발송되었습니다.'}, status=status.HTTP_200_OK)

    @find_password.mapping.post
    def find_password_check(self, request):
        confirm_code = request.data.get('confirm_code')

        user = User.objects.get(confirm_code=confirm_code)
        if not user:
            return Response({'message': False}, status=status.HTTP_404_NOT_FOUND)
        if user.confirm_code != str(confirm_code):
            return Response({'message': False}, status=status.HTTP_400_BAD_REQUEST)
        user.confirm_code = None
        user.save()
        return Response({'message': True}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='reset-password', serializer_class=PasswordCheckSerializer)
    def reset_password(self, request):
        """비밀번호 초기화"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        user = get_object_or_404(User, email=data['email'])
        user.set_password(data['password'])
        user.save()
        return Response({'message': '패스워드가 정상적으로 변경되었습니다.'}, status=status.HTTP_200_OK)




class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request):
        """로그인"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data  # Fetch the data form serializer

        user = authenticate(**data)
        if not user:
            return Response({'message': 'incorrect id or pw, please check again'}, status=status.HTTP_404_NOT_FOUND)

        # Generate Token
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            },
            status=status.HTTP_200_OK
        )
