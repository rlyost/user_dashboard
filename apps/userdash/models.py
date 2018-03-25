from __future__ import unicode_literals
from django.db import models
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    # EMAIL validation
    def email_validator(self, postData):
        errors = {}
        # Validates email address for proper format.
        if len(postData['email']) < 1:
            errors["email"] = "Email cannot be blank!"
            return errors
        elif not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "Invalid Email Address!"
            return errors

    # Checks to see if email is already in Db
    def dbcheck_validator(self, postData):
        errors = {}
        #grabs record if email exists in the Db
        mail_check = User.objects.filter(email=postData['email'])
        if len(mail_check) == 0:
            errors["email"] = "Email not found!"
            return errors

    # Db DUPLICATE validation
    def db_validator(self, postData):
        errors = {}
        mail_check = User.objects.filter(email=postData['email'])
        if len(mail_check) != 0:
            dup_check = User.objects.filter(email=postData['email']).id
            if dup_check != int(postData['id']):
                errors["email"] = "Duplicate address in database, please enter another address."
                return errors

    # NAME validation    
    def name_validator(self, postData):
        errors = {}
        # Checks name fields
        if len(postData['fname']) < 2 or len(postData['lname']) < 2:
            errors["name"] = "Name must be longer."
            return errors
        elif not str(postData['fname']).isalpha():
            errors["name"] = "First Name can only be letters."
            return errors       
        elif not str(postData['lname']).isalpha():
            errors["name"] = "Last Name can only be letters."
            return errors 

    # PASSWORD validation
    def pw_validator(self, postData):
        errors = {}
        # Check password length and matching confirmation
        if len(postData['password']) < 8:
            errors["password"] = "Password is not long enough!"
            return errors
        elif postData['password'] != postData['password2']:
            errors["password"] = "Passwords do not match!"
            return errors

    # HASHED PASSWORD validation
    def hpw_validator(self, postData):
        errors = {}
        if len(postData['password']) > 7:
            log_pass = User.objects.get(email=postData['email']).password
        else:
            errors['email'] = "Please provide a valid password."
            return errors
        #password validation - compares hashed logged in password to hashed Db password
        if not bcrypt.checkpw(postData['password'].encode(), log_pass.encode()):
            errors["email"] = "Password does not match."
            return errors
   
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    desc = models.CharField(max_length=500)
    level = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()

class Post(models.Model):
    message = models.CharField(max_length=500)
    user = models.ForeignKey(User, related_name="poster")
    users = models.ManyToManyField(User, related_name="posts")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Comment(models.Model):
    comments = models.CharField(max_length=255)
    post = models.ForeignKey(Post, related_name="commented")
    user = models.ForeignKey(User, related_name="comments")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)