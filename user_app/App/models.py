from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User (AbstractUser):
    """ Extend User Model """

    first_name = models.CharField (max_length=20)
    last_name = models.CharField (max_length=20)
    date_of_birth = models.DateField (null=True,blank=True)
    email = models.EmailField (unique=True)
    phone_number = models.CharField (max_length=10)
    street = models.CharField (max_length=30)
    zipcode = models.CharField ( max_length=10 )
    city = models.CharField (max_length=20 , null=True)
    state = models.CharField (max_length=20)
    country = models.CharField (max_length=20)
