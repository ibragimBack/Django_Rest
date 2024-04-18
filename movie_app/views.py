from rest_framework.decorators import api_view
from rest_framework.response import Response
from . models import Director, Movie, Review
from . serializers import (DirectorSerializers, DirectorDetailSerializers, MovieSerializers,
                           MovieDetailSerializers, ReviewSerializers, ReviewDetailSerializers)
from rest_framework import status

@api_view(['GET'])
def director_list_api_view(request):
    directors = Director.objects.all()
    list_ = DirectorSerializers(directors, many=True).data
    return Response(data=list_)

@api_view(['GET'])
def director_detail_api_view(request, id):
    try:
        director = Director.objects.get(id=id)
    except Director.DoesNotExist:
        return Response(data={'error': 'Director not found'},
                        status=status.HTTP_404_NOT_FOUND)
    data = DirectorDetailSerializers(director).data
    return Response(data=data)

@api_view(['GET'])
def movie_list_api_view(request):
    movies = Movie.objects.all()
    list_ = MovieSerializers(movies, many=True).data
    return Response(data=list_)

@api_view(['GET'])
def movie_detail_api_view(request, id):
    try:
        movie = Movie.objects.get(id=id)
    except Movie.DoesNotExist:
        return Response(data={'error': 'Movie not found'},
                        status=status.HTTP_404_NOT_FOUND)
    data = MovieDetailSerializers(movie).data
    return Response(data=data)

@api_view(['GET'])
def review_list_api_view(request):
    reviews = Review.objects.all()
    list_ = ReviewSerializers(reviews, many=True).data
    return Response(data=list_)

@api_view(['GET'])
def review_detail_api_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(data={'error': 'Review not found'},
                        status=status.HTTP_404_NOT_FOUND)
    data = ReviewDetailSerializers(review).data
    return Response(data=data)