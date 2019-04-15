from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

"""Declare models for YOUR_APP app."""

from django.contrib.auth.models import AbstractUser, BaseUserManager ## A new class is imported. ##
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.auth.models import User

class My_Favourite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, default=None)
    product_link = models.TextField()
    product_image_link = models.TextField()
    product_name = models.TextField()
    product_price = models.TextField()
    product_tag = models.TextField()

class Search_product(models.Model):
    user =  models.TextField()
    product_link = models.TextField()
    product_image_link = models.TextField()
    product_name = models.TextField()
    product_price = models.TextField()
    selling_website = models.TextField()

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        print('register')
        print(user)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """User model."""

    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()
    def fun_raw_sql_query(**kwargs):
        email = kwargs.get('email')
        if email:
            result = User.objects.raw('SELECT * FROM cover_page_user WHERE email = %s', [email])
        else:
            result = User.objects.raw('SELECT * FROM cover_page_user')
        return result
class Product(models.Model):
    
    product_link = models.TextField()
    product_image_link = models.TextField()
    product_name = models.TextField()
    product_price = models.TextField()
    product_tag = models.TextField()
    def del_recent_product(**kwargs):
        Product.objects.all().delete()
    def sql_all_recent_product(product_tag):
            result = Product.objects.filter(product_tag = product_tag)
            return result
    class Meta:
        db_table = "recent_product"