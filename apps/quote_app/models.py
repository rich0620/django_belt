# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re
import bcrypt
import datetime
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}

        if len(postData['name']) < 3:
            errors['name'] = "Name should be at least 3 characters"

        if User.objects.filter(alias=postData['alias']).count() > 0:
            errors["alias"] = "Alias {} already exists yo".format(postData['alias'])
        if len(postData['alias']) < 3:
            errors['alias'] = "Alias should be at least 3 characters bro"

        if not EMAIL_REGEX.match(postData['email']):
            errors['email_format'] = "Wrong email format dude"
        if User.objects.filter(alias=postData['email']).count() > 0:
            errors["email"] = "Email {} already exists yo".format(postData['email'])

        if len(postData['password']) < 8:
            errors['password_length'] = "Password must be at least 8 characters" 
        if postData['password'] != postData['confirmPW']:
            errors['confirmPW'] = "Passwords do not match"

        if len(postData['dateOfBirth']) > 0:
            today = datetime.datetime.today()
            dateOfBirth = datetime.datetime.strptime(postData['dateOfBirth'],"%Y-%m-%d")
            if dateOfBirth > today:
                errors['dateOfBirth'] = "Seriously? You can't be born in the future"
        else:
            errors['dateOfBirth'] = "date of birth required"

        return errors

    def login_validator(self, postData):
        print "made it to log login_validator"

        errors = {}
        email = postData['email']
        password = postData['password']

        existing_user_list = User.objects.filter(email=email)        #filter() and exclude() are lists / get() will break if nothing is returned
        if len(existing_user_list) > 0:
            if bcrypt.checkpw(password.encode(), (existing_user_list[0].password).encode()):
                return errors

        errors['login_error'] = "must enter valid email/password combo"
        return errors



class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.TextField()
    birthday = models.DateField(auto_now = False, auto_now_add = False, default= '2000-01-01')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
    def __repr__(self):
        return "<User object: {} {} {} {} {} {}>".format(self.name, self.alias, self.password, self.birthday, self.created_at, self.updated_at)

class QuoteManager(models.Manager):
    def addQuote(self, quote_id, user_id):
        me = User.objects.get(id=user_id)
        quote = Quote.objects.get(id=quote_id)
        quote.faved_by.add(me)

    def removeQuote(self, quote_id, user_id):
        me = User.objects.get(id=user_id)
        quote = Quote.objects.get(id=quote_id)
        quote.faved_by.remove(me)

class Quote(models.Model):
    author=models.CharField(max_length=255)
    text=models.TextField(1000)
    posted_by=models.ForeignKey(User,related_name='posted_quote')
    faved_by=models.ManyToManyField(User, related_name='faved_quotes')
    objects = QuoteManager()
    def __repr__(self):
        return "<User object: {}>".format(self.author)
