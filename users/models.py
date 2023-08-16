from django.db import models
from datetime import datetime

import re
import bcrypt

# Create your models here.

class UserManager(models.Manager):
    def validator(self, postData, instance=None):
        errors = {}

        name_regex = re.compile(r'^[a-zA-Z]')
        email_regex = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

        if len(postData['fname']) < 2:
            errors['fname'] = "First Name is required and should be at least 2 characters."
            if not name_regex.match(postData['fname']):
                errors['fname'] = "First Name must have letters only."

        if len(postData['lname']) < 2:
            errors['lname'] = "Last Name is required and should be at least 2 characters."
            if not name_regex.match(postData['lname']):
                errors['lname'] = "Last Name must have letters only."

        if not email_regex.match(postData['email']):
            errors['email'] = "Please enter a valid email address."
        elif instance is None and self.filter(email=postData['email']).exists():
            errors['email'] = "Email is already in use."
        elif instance is not None and self.filter(email=postData['email']).exclude(id=instance.id).exists():
            errors['email'] = "Email is already in use."

        if len(postData['password']) < 8:
            errors['password'] = "Password should be at least 8 characters."

        if postData['password'] != postData['cpassword']:
            errors['cpassword'] = "Passwords do not match."

        return errors


class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
