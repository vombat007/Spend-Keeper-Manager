from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models, IntegrityError


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, username=None, is_staff=False, is_superuser=False):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')

        if User.objects.filter(email=self.normalize_email(email).lower()).exists():
            raise ValueError('This email has already been registered.')

        user = self.model(
            email=self.normalize_email(email).lower(),
            is_staff=is_staff,
            is_superuser=is_superuser
        )

        user.set_password(password)
        try:
            user.save(using=self._db)

        except IntegrityError:
            raise ValueError('This email has already been registered.')

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    objects = MyUserManager()

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        error_messages={
            'unique': "This email has already been registered.",
        }
    )
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        app_label = 'django_app_api'


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    total_balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='category_pics/', null=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return self.name


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    note = models.TextField(blank=True)
    datetime = models.DateTimeField(auto_now_add=True)
    is_income = models.BooleanField(default=False)  # True if income, False if expense

    def __str__(self):
        return f"{self.user.username}'s {'Income' if self.is_income else 'Expense'}: {self.amount} {self.currency}"


class Saving(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='savings')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    note = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username}'s Savings: {self.amount} {self.account}"

