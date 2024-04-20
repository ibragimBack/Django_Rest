from rest_framework import serializers
from . models import Director, Movie, Review

class DirectorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = 'name movies_count'.split()

class DirectorDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = '__all__'

class MovieSerializers(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = 'title duration'.split()

class MovieDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

class ReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'text'.split()

class ReviewDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class MovieReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = 'title duration review rating'.split()
        depth = 1