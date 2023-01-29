from django.core.mail import send_mail
from rest_framework import filters, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from reviews.models import User
from .permissions import IsSuperuser
from .serializers import (MeSerializer, SignUpSerializer, TokenSerializer,
                          UserSerializer)


class UserView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    permission_classes = (IsSuperuser,)

    def get(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return self.list(request, *args, **kwargs)


class UserViewDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsSuperuser,)

    def get(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class MeViewDetail(APIView):
    serializer_class = MeSerializer

    def get(self, request):
        if request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = self.serializer_class(request._user, many=False)
        return Response(serializer.data)

    def patch(self, request):
        if request.user.is_anonymous:
            return Response(status=status.HTTP_403_FORBIDDEN)
        user = User.objects.get(username=request._user)
        serializer = self.serializer_class(
            user,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignUp(APIView):
    serializer_class = SignUpSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = request.data.get('username')
        email = request.data.get('email')
        if not User.objects.filter(username=username, email=email).exists():
            serializer.save()
        user = User.objects.get(username=username)
        if user.confirmation_code != '':
            return Response(status=status.HTTP_200_OK)
        user.confirmation_code = 'test_code'
        user.save()

        send_mail(
            'Confirmation code from YaMDB',
            user.confirmation_code,
            'from@example.com',
            [email],
            fail_silently=False,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class TokenView(APIView):
    serializer_class = TokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = request.data.get('username')
        confirmation_code = request.data.get('confirmation_code')
        if not User.objects.filter(username=username).exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
        user = User.objects.get(username=username)
        if user.confirmation_code == confirmation_code:
            return Response(
                {
                    'token': user.token
                },
                status=status.HTTP_201_CREATED
            )
        return Response(status=status.HTTP_400_BAD_REQUEST)
