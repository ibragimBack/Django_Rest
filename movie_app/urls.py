from django.urls import path
from movie_app import views

urlpatterns = [
    path('directors/', views.DirectorListAPIView.as_view()),
    path('', views.MovieListAPIView.as_view()),
    path('reviews/', views.ReviewListAPIView.as_view()),
    path('directors/<int:id>/', views.DirectorDetailAPIView.as_view()),
    path('<int:id>/', views.MovieDetailAPIView.as_view()),
    path('reviews/<int:id>/', views.ReviewDetailAPIViews.as_view()),
    path('movies/reviews/', views.MovieReviewAPIView.as_view()),
]
