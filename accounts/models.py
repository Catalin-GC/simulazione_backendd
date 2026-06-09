from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("L'email è obbligatoria")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("ruolo", User.Ruolo.RESPONSABILE)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Il superuser deve avere is_staff=True.")
            
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Il superuser deve avere is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    class Ruolo(models.TextChoices):
        DIPENDENTE = "DIPENDENTE", "Dipendente"
        RESPONSABILE = "RESPONSABILE", "Responsabile amministrativo"

    email = models.EmailField("indirizzo email", unique=True)
    nome = models.CharField(max_length=100)
    cognome = models.CharField(max_length=100)
    ruolo = models.CharField(
        max_length=20,
        choices=Ruolo.choices,
        default=Ruolo.DIPENDENTE,
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nome", "cognome"]

    @property
    def is_responsabile(self):
        return self.ruolo == self.Ruolo.RESPONSABILE

    def __str__(self):
        return f"{self.nome} {self.cognome} ({self.email})"
