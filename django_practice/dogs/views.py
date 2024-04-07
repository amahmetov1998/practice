from rest_framework import views
from rest_framework.response import Response

from dogs.models import Dog, Breed
from dogs.serializers import DogSerializer, BreedSerializer


class DogList(views.APIView):
    def get(self, request):
        dogs = Dog.objects.all()
        return Response({'dogs': DogSerializer(dogs, many=True).data})

    def post(self, request):
        serializer = DogSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'dog': serializer.data})


class DogDetail(views.APIView):

    def get(self, request, pk):
        dog = Dog.objects.get(pk=pk)
        return Response({'dog': DogSerializer(dog).data})

    def put(self, request, pk):
        if not pk:
            return Response({"error": "PK is required"})
        try:
            instance = Dog.objects.get(pk=pk)
        except:
            return Response({"error": "Object does not exist"})

        serializer = DogSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'dog': serializer.data})

    def delete(self, request, pk):
        if not pk:
            return Response({"error": "PK is required"})
        try:
            instance = Dog.objects.get(pk=pk)
            instance.delete()
        except:
            return Response({"error": "Object does not exist"})

        return Response({"dog": "Object was deleted"})


class BreedList(views.APIView):

    def get(self, request):
        breeds = Breed.objects.all()
        return Response({'breeds': BreedSerializer(breeds, many=True).data})

    def post(self, request):
        serializer = BreedSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'breeds': serializer.data})


class BreedDetail(views.APIView):

    def get(self, request, pk):
        breed = Breed.objects.get(pk=pk)
        return Response({'breed': BreedSerializer(breed).data})

    def put(self, request, pk):

        if not pk:
            return Response({"error": "PK is required"})
        try:
            instance = Breed.objects.get(pk=pk)
        except:
            return Response({"error": "Object does not exist"})

        serializer = BreedSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'breed': serializer.data})

    def delete(self, request, pk):
        if not pk:
            return Response({"error": "PK is required"})
        try:
            instance = Breed.objects.get(pk=pk)
            instance.delete()
        except:
            return Response({"error": "Object does not exist"})

        return Response({"breed": "Object was deleted"})
