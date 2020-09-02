from __future__ import unicode_literals

from django.db import models
from django.urls import reverse_lazy
import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MaxValueValidator

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null = True)
    student_id = models.PositiveIntegerField(validators=[MaxValueValidator(99999999)], null=True)
    name = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def delete(self, *args, **kwargs):
        self.student_id.delete()
        self.name.delete()
        self.email.delete()
        super(Data, self).delete(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        url = reverse_lazy('detail', kwargs={'pk': self.pk})
        return url


class Group(models.Model):
    no = models.IntegerField(unique=True)

import datetime

def current_year():
    return datetime.date.today().year

def current_sem():
    if datetime.date.today().month < 8 and datetime.date.today().month > 1:
        return 1
    else:
        return 2

class Year(models.Model):
    year = models.IntegerField()

class Data(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    year = models.ForeginKey(Year)
    sem = models.IntegerField(default=current_sem)
    image = models.ImageField(upload_to='%Y/%m/%d/orig')
    title = models.CharField(max_length=100, blank=True, null=True)
    text = models.TextField(null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null = True)
    participator = models.ManyToManyField(User)
    code = models.IntegerField(blank=True, null=True)
    code_when_saved = models.DateTimeField(null=True, blank=True)
    study_start_time = models.CharField(max_length=100, blank=True, null=True)
    study_total_duration = models.IntegerField(default=0)

    def delete(self, *args, **kwargs):
        self.image.delete()
        self.filtered_image.delete()
        super(Data, self).delete(*args, **kwargs)

    def get_absolute_url(self):
        url = reverse_lazy('detail', kwargs={'pk': self.pk})
        return url

class UserInfo(models.Model):
    year = models.ForeginKey(Year)
    sem = models.IntegerField(default=current_sem)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ManyToManyField(User)

class Announcement(models.Model):
    author = models.TextField(max_length=100)
    date = models.DateTimeField(default=timezone.now)
    title = models.TextField(max_length=100)
    content = models.TextField()

    def delete(self, *args, **kwargs):
        self.author.delete()
        self.date.delete()
        self.title.delete()
        self.content.delete()
        super(Announcement, self).delete(*args, **kwargs)

    def get_absolute_url(self):
        url = reverse_lazy('announce_detail', kwargs={'pk': self.pk})
        return url


class Verification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.IntegerField(null=True, blank=True)
    code_when_saved = models.DateTimeField(null=True, blank=True)

@receiver(post_save, sender=User)
def create_user_verification(sender, instance, created, **kwargs):
    if created:
        Verification.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_verification(sender, instance, **kwargs):
    instance.verification.save()
