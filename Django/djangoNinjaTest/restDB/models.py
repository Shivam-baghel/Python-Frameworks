from django.db import models
from django.core.validators import MaxValueValidator,MinValueValidator
from django.contrib.auth.models import User

# Create your models here.

class StreamPlatform(models.Model):
    name = models.CharField(max_length=30)
    about = models.CharField(max_length=150)
    website = models.URLField(max_length=100)
    
    def __str__(self):
        return self.name


class WatchList(models.Model):
    title = models.CharField(max_length=50)
    storyline = models.CharField(max_length=200)
    # many to one relationship
    platform = models.ForeignKey(StreamPlatform, on_delete=models.CASCADE, related_name='watchlist' )
    
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    

class Review(models.Model):
    
    review_user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    description = models.CharField(max_length=300, null=True)
    watchlist = models.ForeignKey(WatchList, on_delete=models.CASCADE, related_name='reviews')
    active = models.BooleanField(default=True)
    #auto_now_add is used to record the datetime when model instance is created.
    created = models.DateTimeField(auto_now_add=True)
    #auto_now is used to automatically update the filed with the current date and time whenever model's save method is called.
    update = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.rating) + " stars - " + self.watchlist.title
