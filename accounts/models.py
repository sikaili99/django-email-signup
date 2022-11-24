
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (
    BaseUserManager, 
    AbstractBaseUser, 
    PermissionsMixin,
    )
from django.utils import timezone
from django.db import models

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, phonenumber, password, **extra_fields):
        """Create and save a User with the given phonenumber and password."""
        if not phonenumber:
            raise ValueError('The given phonenumber must be set')
        user = self.model(phonenumber=phonenumber, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phonenumber, password=None, **extra_fields):
        """Create and save a regular User with the given phonenumber and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phonenumber, password, **extra_fields)

    def create_superuser(self, phonenumber, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phonenumber, password, **extra_fields)


class AbstractUser(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username and password are required. Other fields are optional.
    """
    phonenumber = models.CharField(
        _('phonenumber'),
        max_length=20,
        unique=True,
        validators=[],
        error_messages={
            'unique': _("A user with that phone number already exists."),
        },
    )
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'phonenumber'
    REQUIRED_FIELDS = ['email','phonenumber']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

class CustomUser(AbstractUser):
    """Custom user model."""
    phonenumber = models.CharField(_('phone number'),max_length=20, unique=True)

    USERNAME_FIELD = 'phonenumber'
    REQUIRED_FIELDS = []
