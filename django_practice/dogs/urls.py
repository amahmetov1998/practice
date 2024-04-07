from django.urls import path

from dogs import views

urlpatterns = [
    path('dogs/', views.DogList.as_view()),
    path('dogs/<int:pk>/', views.DogDetail.as_view()),
    path('breeds/', views.BreedList.as_view()),
    path('breeds/<int:pk>/', views.BreedDetail.as_view()),
]
