from django.db import models


class Dog(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    breed = models.ForeignKey('Breed', on_delete=models.CASCADE)
    gender = models.CharField(max_length=20)
    color = models.CharField(max_length=50)
    favorite_food = models.CharField(max_length=200)
    favorite_toy = models.CharField(max_length=50)


class Status(models.TextChoices):
    SMALL = 'Small', 'S'
    TINY = 'Tiny', 'T'
    Medium = 'Medium', 'M'
    LARGE = 'Large', 'L'


class Breed(models.Model):
    name = models.CharField(max_length=50)
    size = models.CharField(max_length=10, choices=Status.choices)
    friendliness = models.IntegerField()
    trainability = models.IntegerField()
    shedding_amount = models.IntegerField()
    exercise_needs = models.IntegerField()

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(size__in=Status.values), name='size'),
            models.CheckConstraint(check=models.Q(friendliness__in=list(range(1, 6))), name='friendliness'),
            models.CheckConstraint(check=models.Q(trainability__in=list(range(1, 6))), name='trainability'),
            models.CheckConstraint(check=models.Q(shedding_amount__in=list(range(1, 6))), name='shedding_amount'),
            models.CheckConstraint(check=models.Q(exercise_needs__in=list(range(1, 6))), name='exercise_needs'),
        ]
