from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from .serializers import UserSerializer
from django.contrib.auth.models import User

class UserList(ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserDetail(RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
