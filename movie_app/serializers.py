from rest_framework import serializers
from .models import Director, Movie, Review
from rest_framework.exceptions import ValidationError


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


class DirectorValidateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100, min_length=2)


class MovieValidateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255, min_length=3)
    description = serializers.CharField(max_length=255, min_length=10)
    duration = serializers.FloatField(min_value=40)
    director_id = serializers.IntegerField()

    def validate_director_id(self, director_id):
        try:
            Director.objects.get(id=director_id)
        except Director.DoesNotExist:
            raise ValidationError("Director not found!")
        return director_id


class ReviewValidateSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=255)
    movie_id = serializers.IntegerField()
    star = serializers.IntegerField(min_value=1, max_value=5)

    def validate_movie_id(self, movie_id):
        try:
            Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist:
            raise ValidationError("Movie not found!")
        return movie_id