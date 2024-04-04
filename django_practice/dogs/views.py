from rest_framework import generics, viewsets, mixins

from dogs.models import Dog, Breed
from dogs.serializers import DogSerializer, BreedSerializer


class DogList(generics.ListCreateAPIView):
    queryset = Dog.objects.all()
    serializer_class = DogSerializer


class DogDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Dog.objects.all()
    serializer_class = DogSerializer


class BreedList(mixins.CreateModelMixin,
                mixins.ListModelMixin,
                viewsets.GenericViewSet):

    queryset = Breed.objects.all()
    serializer_class = BreedSerializer


class BreedDetail(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):

    queryset = Breed.objects.all()
    serializer_class = BreedSerializer
