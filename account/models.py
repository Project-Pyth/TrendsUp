from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator  # Validation for Phone number


# UserProfile Model
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Links With User Model
    description = models.TextField(max_length=1000, default='', blank='True')
    city = models.CharField(max_length=100, default='', blank='True')
    ph = RegexValidator(regex=r'^\+?1?\d{10,15}$', message="Enter in format +9999999999. Upto 15 digits allowed")
    phone = models.CharField(validators=[ph], max_length=17, blank=True)
    image = models.ImageField(upload_to='profile_image', default='default.jpg', blank=True, null=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
