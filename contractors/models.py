from django.db import models
from django.conf import settings
from users.models import User

import re
import random
import string
import os

from decimal import Decimal
from datetime import datetime

# Create your models here.

class ContractorManager(models.Manager):

    def validator(self, postData, instance=None):
        errors = {}

        email_regex = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        mobile_regex =re.compile(r'(\+?\d{2}?\s?\d{3}\s?\d{3}\s?\d{4})|([0]\d{3}\s?\d{3}\s?\d{4})')

        if len(postData['company_name']) < 2:
            errors['company_name'] = "Company Name is required and should be at least 2 characters."

        if not email_regex.match(postData['email']):
            errors['email'] = "Please enter a valid email address."
        elif instance is None and (self.filter(email=postData['email']).exists() or User.objects.filter(email=postData['email']).exists()):
            errors['email'] = "Email is already in use."
        elif instance is not None and (self.filter(email=postData['email']).exclude(id=instance.id).exists() or User.objects.filter(email=postData['email']).exists()):
            errors['email'] = "Email is already in use."

        if len(postData['specialization']) < 3:
            errors['specialization'] = "Specialization is required and should be at least 3 characters"

        if not mobile_regex.match(postData['mobile']):
            errors['mobile'] = "Please enter a valid mobile phone number."

        if 'password' in postData:
            if len(postData['password']) < 8:
                errors['password'] = "Password should be at least 8 characters."

            if postData['password'] != postData['cpassword']:
                errors['cpassword'] = "Passwords do not match."

        return errors

class Contractor(models.Model):
    company_name = models.CharField(max_length=45)
    email = models.EmailField(max_length=255, unique=True)
    specialization = models.CharField(max_length=45)
    mobile = models.CharField(max_length=20)
    landline = models.CharField(max_length=20, null=True, blank=True)
    password = models.CharField(max_length=128)
    is_contractor = models.BooleanField(default=True)
    company_description = models.TextField(null=True, blank=True, default="")
    logo = models.ImageField(upload_to="logos/",null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ContractorManager()

    def remove_logo(self):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.logo.path))
        self.logo = None
        self.save()


class ProjectManager(models.Manager):
    def validator(self, postData, instance=None):
        errors = {}

        decimal_regex = re.compile('^[0-9]+(\.[0-9]+)?$')
        if len(postData['project_name']) < 2:
            errors['project_name'] = "Project Name is required and should be at least 2 characters."
        elif instance is None and self.filter(project_name=postData['project_name']).exists():
            errors['project_name'] = "Project Name already exists."
        elif instance is not None and self.filter(project_name=postData['project_name']).exclude(id=instance.id).exists():
            errors['project_name'] = "Project Name already exists."

        if len(postData['project_description']):
            if len(postData['project_description']) < 10:
                errors['project_description'] = "Project Description should be at least 10 characters."
        
        if not postData['project_cost']:
            errors['project_cost'] = "Please input a valid cost."
        elif not decimal_regex.match(postData['project_cost']):
            errors['project_cost'] = "Please input a valid cost."
        elif Decimal(postData['project_cost']) < 0:
            errors['project_cost'] = "Please input a valid cost."

        try:
            completion_date = datetime.strptime(postData['completion_date'], '%Y-%m-%d').date()
            if completion_date <= datetime.now().date():
                errors['completion_date'] = "Completion date must not be in the past."
        except ValueError:
            errors['completion_date'] = "Please include a valid date."
        return errors
    
    def create(self, **kwargs):
        if 'project_code' not in kwargs:
            kwargs['project_code'] = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

        return super().create(**kwargs)


class Project(models.Model):
    contractor = models.ForeignKey(Contractor, related_name='projects', on_delete=models.CASCADE)
    owners = models.ManyToManyField(User, related_name='projects')
    project_name = models.CharField(max_length=45)
    project_description = models.TextField()
    project_cost = models.DecimalField(max_digits=10, decimal_places=2)
    project_code = models.CharField(max_length=5, unique=True, default="")
    completion_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ProjectManager()


class UpdateManager(models.Manager):
    def validator(self, postData, instance=None):
        errors = {}

        if len(postData['update_description']) < 10:
            errors['update_description'] = "Description is required and should be at least 10 characters."

        try:
            date = datetime.strptime(postData['date'], '%Y-%m-%d').date()
            if date > datetime.now().date():
                errors['date'] = "Date of update must not be in the future."
        except ValueError:
            errors['date'] = "Invalid date format."
        return errors

class Update(models.Model):
    project = models.ForeignKey(Project, related_name="updates", on_delete=models.CASCADE)
    update_description = models.TextField()
    date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UpdateManager()

class Photos(models.Model):
    contractor = models.ForeignKey(Contractor, related_name="photos", on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, related_name='photos', on_delete=models.CASCADE, null=True)
    update = models.ForeignKey(Update, related_name='photos', on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='photos/')
    caption = models.TextField(null=True)

    def delete(self, *args, **kwargs):
        if self.image:
            os.remove(os.path.join(settings.MEDIA_ROOT, self.image.path))

        super(Photos, self).delete(*args, **kwargs)

