from django.contrib.auth.models import AbstractUser
from django.db import models

#pilar2@pilar.com 5pGabST7wYpeAnj
#p3@pilar.com 5pGabST7wYpeAnj


class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Administrador'),
        ('user', 'Usuari del Gimnàs'),
        ('trainer', 'Entrenador'),
        ('director', 'Director')
    ]

    email = models.EmailField(
        unique=True,
        help_text='Required. 254 characters or fewer. Letters, digits and @/./+/-/_ only.',
        max_length=254)
    first_name = models.CharField(
        max_length=30,
        help_text='Required. 30 characters or fewer. Letters, digits and ./+/-/_ only.')
    last_name = models.CharField(
        max_length=30,
        help_text='Required. 30 characters or fewer. Letters, digits and ./+/-/_ only.')
    role = models.CharField(
        max_length=10, 
        choices=ROLE_CHOICES, 
        default='user',
        help_text='Tipus d\'usuari')
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'role']
    
    class Meta:
        db_table = 'users'


    def __str__(self):
        return f"{self.first_name} {self.last_name}"
