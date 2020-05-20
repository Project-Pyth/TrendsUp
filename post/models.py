from datetime import datetime

from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.db.models.signals import pre_save, post_delete
from django.utils import timezone
from django.utils.text import slugify
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils.timezone import now


# Upload Location/Directory Making
def upload_location(instance, filename):  # Post path in Url
    file_path = 'detail/{category}/{title}-{filename}'.format(
        category=str(instance.category), title=str(instance.title), filename=filename
    )
    return file_path


# Model For Categories
class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


# Model For Posts
class Post(models.Model):
    title = models.CharField(max_length=200, blank=False, null=False)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.CASCADE)
    body = RichTextUploadingField(max_length=10000, blank=False, null=False)
    image = models.ImageField(upload_to=upload_location, blank=False, null=False)
    date_posted = models.DateTimeField(default=now)
    author = models.ForeignKey(User, default=None, blank=True, null=True, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255, blank=True, unique=True)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        return self.title


@receiver(post_delete, sender=Post)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.author.username + '-' + instance.title)


pre_save.connect(pre_save_post_receiver, sender=Post)


# Post Comments Model
class PostComment(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return self.comment[0:20] + '.....' + 'by ' + self.user.username
