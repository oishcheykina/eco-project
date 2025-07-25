from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class Achievement(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.ImageField(upload_to='achievements/icons/', null=True, blank=True)
    reward = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email обязателен")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        
        extra_fields.setdefault('is_active', True)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)  # <--- ВАЖНО!
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    balance = models.PositiveIntegerField(default=0)
    achievements = models.ManyToManyField(Achievement, blank=True, related_name='users')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    
    def get_full_name(self):
        return self.full_name


class Tree_Type(models.Model):
    name = models.CharField(max_length=50)
    cost = models.PositiveIntegerField()
    emit_oxygen = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, blank=True, null=True)
    utilize_carbon = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, blank=True, null=True)

    def __str__(self):
        return self.name


class Tree(models.Model):
    tree_type = models.ForeignKey(Tree_Type, on_delete=models.CASCADE, related_name='trees')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='trees')
    photo_initial = models.ImageField(upload_to='trees/initial/')
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    date_planted = models.DateField(auto_now_add=True)
    photo_confirmation = models.ImageField(upload_to='trees/confirmation/', null=True, blank=True)
    date_confirmed = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.tree_type} by {self.user.email}"  # или self.user.full_name

    def get_absolute_url(self):
        return reverse("tree_detail", kwargs={"tree_id": self.id})
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_user_balance()

    def update_user_balance(self):
        user = self.user
        total = sum(tree.tree_type.cost for tree in Tree.objects.filter(user=user))
        user.balance = total
        user.save()

# models.py
import uuid
from django.utils import timezone
from datetime import timedelta

class EmailVerificationCode(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return self.created_at < timezone.now() - timedelta(minutes=10)

    def __str__(self):
        return f"{self.email} - {self.code}"
