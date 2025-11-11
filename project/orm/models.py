from decimal import Decimal
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username=None, password=None, **extra_fields):
        if not email:
            raise ValueError("Email обязателен")
        email = self.normalize_email(email)
        if username is None:
            username = email.split("@")[0]
        extra_fields.setdefault('is_active', True)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', CustomUser.Role.ADMIN)
        if username is None:
            username = email.split("@")[0]
        return self.create_user(email, username=username, password=password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        ADMIN = "admin", "Admin"
        MANAGER = "manager", "Manager"
        EMPLOYEE = "employee", "Employee"

    class Department(models.TextChoices):
        HR = "hr", "Human Resources"
        IT = "it", "Information Technology"
        SALES = "sales", "Sales"
        MARKETING = "marketing", "Marketing"
        FINANCE = "finance", "Finance"

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)

    phone = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, blank=True)
    department = models.CharField(max_length=100, null=True, blank=True, choices=Department.choices)

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.EMPLOYEE)

    birth_date = models.DateField(null=True, blank=True)
    salary = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))

    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return f"""{self.email}, {self.username}, {self.first_name} {self.last_name}, {self.role}, 
            {self.department}, {self.phone}, {self.city}, {self.country}, {self.birth_date}, {self.salary}, 
            {self.date_joined}, {self.is_active}, {self.is_staff}, {self.last_login}
        """

    class Meta:
        verbose_name = "Custom user"
        verbose_name_plural = "Custom users"
