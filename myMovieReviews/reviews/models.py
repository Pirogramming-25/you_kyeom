from django.db import models

class MovieReview(models.Model):

    GENRE_CHOICES = [
        ('action', 'Action'),
        ('comedy', 'Comedy'),
        ('drama', 'Drama'),
        ('romance', 'Romance'),
        ('thriller', 'Thriller'),
        ('horror', 'Horror'),
        ('sf', 'SF'),
    ]

    title = models.CharField(max_length=100)            
    release_year = models.IntegerField()            
    director = models.CharField(max_length=100)     
    actor = models.CharField(max_length=200)        
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES,)         
    rating = models.FloatField()                    
    running_time = models.IntegerField()            
    content = models.TextField()                    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title