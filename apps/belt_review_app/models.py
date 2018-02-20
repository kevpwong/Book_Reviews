from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        if len(postData['name']) < 2:
            errors["name"] = "Name needs more than 2 characters"
        if len(postData['alias']) < 2:
            errors["alias"] = "Alias needs more than 2 chalracters"
        if len(postData['email']) < 1:
            errors["email"] = "Email cannot be blank!"
        if not EMAIL_REGEX.match(postData['email']):
            errors["emailinvalid"] = "Invalid Email Address!"
        if len(postData['pass']) < 8:
            errors["passwordlen"] = "Password must be longer than 8 characters"
        if postData['pass'] != postData['confirm']:
            errors["passwordmatch"] = "Passwords do not match"
        if User.objects.filter(email=postData['email']):
            errors["emailexists"] = "Email already exits"
        return errors 
    def login_validator(self, postData):
        errors = {}
        if not User.objects.filter(email=postData['logemail']):
            errors["logemail"] = "Email does not exist in database"
        else:
            if not bcrypt.checkpw(postData['logpass'].encode(), User.objects.filter(email=postData['logemail'])[0].password.encode()):
                errors["wrongpass"] = "Email and Password do not match"
        return errors 

class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    users = models.ForeignKey(User, related_name="user_books")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Review(models.Model):
    rating = models.IntegerField()
    descr= models.TextField()
    books = models.ForeignKey(Book, related_name="book_reviews")
    users = models.ForeignKey(User, related_name="user_reviews")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
