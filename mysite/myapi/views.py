from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from allauth.account.forms import SignupForm
from allauth.account.utils import complete_signup
from allauth.account import app_settings as allauth_settings


from .serializers import User, UserSerializer, UserRegistrationSerializer, LoginFormDataSerializer
from .models import Block, BlockSerializer, LoginFormData
from .forms import CustomUser


class BlockViewSet(viewsets.ModelViewSet):
    queryset = Block.objects.all().order_by('title')
    serializer_class = BlockSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = BlockSerializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()
    
   


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        request = self.request
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(self.request)
            complete_signup(request, user, allauth_settings.EMAIL_VERIFICATION, None)
            serializer.instance = user
        else:
            serializer.is_valid(raise_exception=True)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(request)
            complete_signup(request, user, allauth_settings.EMAIL_VERIFICATION, None)
            return Response({'id': user.id}, status=status.HTTP_201_CREATED)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'])
    def create_user_with_login_data(self, request, *args, **kwargs):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        login_data = CustomUser.create_user_with_login_data(username, email, password)
        serializer = UserRegistrationSerializer(login_data.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginFormDataViewSet(viewsets.ModelViewSet):
    queryset = LoginFormData.objects.all()
    serializer_class = LoginFormDataSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)