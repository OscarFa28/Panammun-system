from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission, BaseUserManager, PermissionsMixin
from django.conf import settings
from django.contrib.auth.hashers import make_password

class Panammun_edition(models.Model):
    name = models.CharField(max_length=20)
    start_registration_date = models.DateTimeField(null=True)
    start_choose_date = models.DateTimeField(null=True)
    start_mun_date = models.DateTimeField(null=True)
    notes = models.TextField(blank=True, null=True)
    actual = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.actual:
            Panammun_edition.objects.filter(actual=True).update(actual=False)
        super(Panammun_edition, self).save(*args, **kwargs)
        

class Committee(models.Model):
    name = models.CharField(max_length=50)
    language = models.CharField(max_length=3)
    panammun_edition = models.ForeignKey(Panammun_edition, on_delete=models.CASCADE, related_name='committees')
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
class Country(models.Model):
    name = models.CharField(max_length=50)
    notes = models.TextField(blank=True, null=True)
    committee = models.ForeignKey(Committee, on_delete=models.CASCADE, related_name='countries')

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    NORMAL_USER = 'normal_user'
    ADMINISTRATOR = 'administrator'
    
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    phone_number_2 = models.CharField(max_length=15, blank=True, null=True)
    
    ACCOUNT_TYPE_CHOICES = [
        (NORMAL_USER, 'Normal_user'),
        (ADMINISTRATOR, 'Administrator'),
    ]
    
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPE_CHOICES, blank=True, null=True)
    school = models.CharField(max_length=20, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    panammun_edition = models.ForeignKey(Panammun_edition, on_delete=models.SET_NULL, related_name='users', blank=True, null=True)
    committee_staff = models.ForeignKey(Committee, on_delete=models.SET_NULL, related_name='users', blank=True, null=True)
    country = models.OneToOneField(Country, on_delete=models.SET_NULL, related_name='users', blank=True, null=True)
    voucher = models.ImageField(upload_to='images/vouchers', blank=True, null=True)
    verified = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def save(self, *args, **kwargs):
        if self.pk and not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.username
    