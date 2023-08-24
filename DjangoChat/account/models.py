from django.contrib.auth.models import AbstractUser
from django.db import models


# extend the AbstractUser model
# we're inheriting all the functionalities of the normal User model, and then we can utilize that and extend as we need
class Account(AbstractUser):
    pass
