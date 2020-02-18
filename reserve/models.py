# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator


class Book(models.Model):
    validators = [
        MaxValueValidator(10000),
        MinValueValidator(0)
    ]
    title = models.CharField(max_length=200)
    pub_date = models.PositiveIntegerField(
        verbose_name='publication date', null=True, blank=True, validators=validators)
    edition = models.PositiveIntegerField(
        null=True, blank=True, validators=validators)
    volume = models.PositiveIntegerField(
        null=True, blank=True, validators=validators)
    authors = models.ManyToManyField('Author', null=True, blank=True)
    user = models.ForeignKey(
        to=User, on_delete=models.PROTECT, null=True, blank=True)
    publication = models.ForeignKey(
        to='Publication', on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.title


class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Publication(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True)
    phone = models.IntegerField(
        null=True, verbose_name='phone number')

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
