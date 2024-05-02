from django.urls import path
from movie_app import views

urlpatterns = [
    path('directors/', views.director_list_api_view),
    path('', views.movie_list_api_view),
    path('reviews/', views.review_list_api_view),
    path('directors/<int:id>/', views.director_detail_api_view),
    path('<int:id>/', views.movie_detail_api_view),
    path('reviews/<int:id>/', views.review_detail_api_view),
    path('movies/reviews/', views.movies_reviews_api_view),
]
