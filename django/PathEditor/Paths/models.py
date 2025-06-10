from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver

class Background(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="backgrounds")
    def __str__(self):
        return self.title
    class Meta:
        ordering = ['title']

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    selected_background = models.ForeignKey(
        Background,
        on_delete=models.SET_NULL,
        null=True,
    )

    def __str__(self):
        return self.user.username

class GameBoard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    rows = models.PositiveIntegerField()
    cols = models.PositiveIntegerField()
    
class Dot(models.Model):
    board = models.ForeignKey(GameBoard, on_delete=models.CASCADE, related_name='dots')
    row = models.PositiveIntegerField()
    col = models.PositiveIntegerField()
    color = models.CharField(max_length=7) 

class DotsJSON(models.Model):
    dots = models.JSONField()
    
class BoardPoint(models.Model):
    board = models.ForeignKey(GameBoard, on_delete=models.CASCADE, related_name='board_points')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_board_points')
    row = models.PositiveIntegerField()
    col = models.PositiveIntegerField()
    order = models.PositiveBigIntegerField()


def get_default_superuser():
    return User.objects.filter(is_superuser=True).first().id

class Path(models.Model):
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE,
        default=get_default_superuser,
        related_name="paths"
    )
    title = models.CharField(max_length=100)
    background = models.ForeignKey(to=Background, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
        
        

class Point(models.Model):
    x = models.IntegerField()
    y = models.IntegerField()
    order = models.PositiveIntegerField()
    path = models.ForeignKey(to=Path, on_delete=models.CASCADE, related_name="points")

    def __str__(self):
        return f"Point ({self.x}, {self.y}) number: {self.order} of {self.path.title}"

    class Meta:
        unique_together = ['order', 'path']


class UserSelection(models.Model):
    selected_image = models.ForeignKey(Background, on_delete=models.CASCADE, null=True)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
    else:
        UserProfile.objects.create(user=instance)