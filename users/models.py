from django.utils.crypto import get_random_string


from django.db import models
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyAccountManager(BaseUserManager):

    def create_user(self, email, username, password=None):
        
        if not email:
            raise ValueError("Users must have an email address.")
        if not username:
            raise ValueError("Users must have a username.")
        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, password):

        user = self.create_user(
            email = self.normalize_email(email),
            username = username
        )
        user.set_password(password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class UserAccount(AbstractBaseUser):

    email             = models.EmailField(verbose_name='email', max_length=70, unique=True)
    username          = models.CharField(max_length=30, unique=True)
    first_name        = models.CharField(max_length=100, null=True, blank=True)
    last_name         = models.CharField(max_length=100, null=True, blank=True)
    date_joined       = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login        = models.DateTimeField(verbose_name='last login', auto_now=True)
    slug              = models.SlugField(blank=True)
    is_admin          = models.BooleanField(default=False)
    is_active         = models.BooleanField(default=True)
    is_staff          = models.BooleanField(default=False)
    is_superuser      = models.BooleanField(default=False)
    hide_email        = models.BooleanField(default=True)
    account_activated = models.BooleanField(default=False)

    objects         = MyAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    # Add Slug creating/checking to save method.  
    def save(self, *args, **kwargs): 
        slug_save(self) 
        super(UserAccount, self).save(*args, **kwargs)


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )



# FUNCTION THAT GENERATES RANDOM 8 CHAR SLUGS AND CHECKS IF IT IS UNIQUE
def slug_save(obj):

  if not obj.slug: # if there isn't a slug
    obj.slug = get_random_string(8) # create one
    slug_is_wrong = True  
    while slug_is_wrong: # keep checking until we have a valid slug
        slug_is_wrong = False
        other_objs_with_slug = type(obj).objects.filter(slug=obj.slug)
        if len(other_objs_with_slug) > 0:
            # if any other objects have current slug
            slug_is_wrong = True
        if slug_is_wrong:
            # create another slug and check it again
            obj.slug = get_random_string(8)