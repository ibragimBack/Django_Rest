from django.db import models
from django.db.models import Avg

# Create your models here.
class Director(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def movies_count(self):
        return Movie.objects.filter(director=self).count()


class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=255)
    duration = models.PositiveIntegerField()
    director = models.ForeignKey(Director, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    '''снизу функция выводид средний балл каждого фильма'''
    def rating(self):
        return self.review.aggregate(Avg('star'))['star__avg']
    '''а функция ниже выводит срдений балл всех фильмов'''
    # def rating(self):
    #     movies = Movie.objects.all()
    #     average_ratings = {}
    #     for movie in movies:
    #         reviews = Review.objects.filter(movie=movie)
    #         avg_rating = reviews.aggregate(Avg('star'))['star__avg']
    #         average_ratings['movie'] = avg_rating
    #     return average_ratings


class Review(models.Model):
    text = models.TextField(max_length=255)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='review')
    star = models.IntegerField(default=1, choices=[(i, i) for i in range(1, 6)], null=True)

    def __str__(self):
        return self.text
