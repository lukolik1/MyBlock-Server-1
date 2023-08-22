from django.db import models
from django.contrib.auth.models import Group
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import viewsets
from django.utils.translation import gettext_lazy as _
 

from .castomUser import CustomUser
from .serializers import BlockSerializer

# Модель для данных страницы
class Block(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=255)

    def __str__(self):
        return self.title






class BlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        fields = '__all__'

class BlockViewSet(viewsets.ModelViewSet):
    queryset = Block.objects.all()
    serializer_class = BlockSerializer

    @action(detail=True, methods=['GET'])
    def by_slug(self, request, slug=None):
        block = get_object_or_404(Block, slug=slug)
        serializer = BlockSerializer(block)
        return Response(serializer.data)

# Модель для хранения данных формы авторизации
class LoginFormData(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=128)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, editable=True)  # Используем CustomUser вместо User

    def __str__(self):
        return self.email
    

    






class BlockViewSet(viewsets.ModelViewSet):
    queryset = Block.objects.all().order_by('title')
    serializer_class = BlockSerializer

    @action(detail=True, methods=['GET'])
    def by_slug(self, request, slug=None):
        block = get_object_or_404(Block, slug=slug)
        serializer = BlockSerializer(block)
        return Response(serializer.data)

    def assign_group_to_user(self, user_id):
        my_group = Group.objects.create(name='My Group')

        user = CustomUser.objects.get(pk=user_id)  # Используем CustomUser вместо User
        user.groups.add(my_group)



