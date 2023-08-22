from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .models import Block, LoginFormData
from .castomUser import CustomUser

class BlockAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content')

    

class CustomUserAdmin(UserAdmin):
    list_display = ('email',  'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'groups')


class LoginFormdataAdmin(admin.ModelAdmin):  
    list_display = ('id', 'email', 'password', 'user') 
# Отмените регистрацию групповой модели по умолчанию
admin.site.unregister(Group)

# Зарегистрируйте модели с помощью пользовательских конфигураций администратора
admin.site.register(Block, BlockAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(LoginFormData, LoginFormdataAdmin)

