from django.db import models
from django.contrib.auth.models import AbstractUser
from taggit.managers import TaggableManager
from django.urls import reverse
# Create your models here.

class User(AbstractUser):
    date_of_birth = models.DateField(verbose_name='تاریخ تولد', blank=True, null=True)
    bio = models.TextField(verbose_name='بایو', blank=True, null=True)
    photo = models.ImageField(upload_to='account_images/', blank=True, null=True)
    job = models.CharField(max_length=250, verbose_name='شغل', blank=True, null=True)
    phone = models.CharField(max_length=11, blank=True, null=True)


class Post(models.Model):
    # relations
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_posts', verbose_name="نویسنده")
    # data fields
    description = models.TextField(verbose_name="توضیحات")
    # date
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    tags = TaggableManager()

    class Meta:
        ordering = ['-created']
        indexes = [models.Index(fields=['-created'])]
        verbose_name_plural = "پست ها"

    def __str__(self):
        return self.author.first_name

    def get_absolute_url(self):
        return reverse('social:post_detail', args=[self.id])