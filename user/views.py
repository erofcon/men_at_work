from django.db.models import Q
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response
from men_at_work.permissions import UserHasAccess
from .serializers import MyTokenObtainPairSerializer, CustomUserSerializer
from user.models import CustomUser


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class GetRelatedUser(APIView):
    """
    Получить связанного пользователья
    """

    permission_classes = [UserHasAccess]

    def get(self, request):
        users = CustomUser.objects.filter(Q(groups__in=request.user.groups.all()) & Q(is_executor=True))
        serializer = CustomUserSerializer(users, many=True)

        return Response(serializer.data)
