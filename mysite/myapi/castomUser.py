import re
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
from django.contrib.auth.models import UserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.contrib.auth.password_validation import validate_password


class CustomUserManager(UserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user




class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    


     

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, username, password, **extra_fields)



class CustomUser(AbstractUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)  # Add this line to create an automatic ID field
    email = models.EmailField(_('email address'), unique=False, blank=True, null=True)  # Change unique to True
    username = models.CharField(_('username'), max_length=30, unique=False)  # Add this line

    objects = CustomUserManager()
    groups = models.ManyToManyField(Group, related_name='custom_users')
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name='custom_users_permissions',
        help_text=_('Specific permissions for this user.'),
    )
    is_custom_superuser = models.BooleanField(
        _('custom superuser status'),
        default=False,
        help_text=_(
            'Designates whether this user has the custom superuser privileges.'
        ),
    )
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username' 
    REQUIRED_FIELDS = []
   



    def clean(self):
        super().clean()
        self.clean_email()
        self.clean_password()

    def clean_email(self):
       if self.email:
        email_validator = EmailValidator()
        try:
            email_validator(self.email)
        except ValidationError:
            raise ValidationError(_('Invalid email'))
    
    
    
    def clean_password(self):
        if self.password:
            try:
                validate_password(self.password, self)
            except ValidationError as e:
             raise ValidationError({'password': ['Пароль слишком короткий. Он должен содержать как минимум 8 символов.']})

    def __str__(self):
        return self.email