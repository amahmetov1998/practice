from rest_framework import serializers
from dogs.models import Dog, Breed


class DogSerializer(serializers.Serializer):
    name = serializers.CharField()
    age = serializers.IntegerField()
    breed_id = serializers.IntegerField()
    gender = serializers.CharField()
    color = serializers.CharField()
    favorite_food = serializers.CharField()
    favorite_toy = serializers.CharField()

    def create(self, validated_data):
        return Dog.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.age = validated_data.get('age', instance.age)
        instance.breed_id = validated_data.get('breed_id', instance.breed_id)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.color = validated_data.get('color', instance.color)
        instance.favorite_food = validated_data.get('favorite_food', instance)
        return instance


class BreedSerializer(serializers.Serializer):
    name = serializers.CharField()
    size = serializers.CharField()
    friendliness = serializers.IntegerField()
    trainability = serializers.IntegerField()
    shedding_amount = serializers.IntegerField()
    exercise_needs = serializers.IntegerField()

    def create(self, validated_data):
        return Dog.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.size = validated_data.get('age', instance.size)
        instance.name = validated_data.get('name', instance.name)
        instance.friendliness = validated_data.get('breed_id', instance.friendliness)
        instance.trainability = validated_data.get('gender', instance.trainability)
        instance.shedding_amount = validated_data.get('color', instance.shedding_amount)
        instance.exercise_needs = validated_data.get('favorite_food', instance.exercise_needs)
        return instance
