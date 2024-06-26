# Generated by Django 5.0.3 on 2024-04-03 08:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Breed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('size', models.CharField(max_length=6)),
                ('friendliness', models.IntegerField()),
                ('trainability', models.IntegerField()),
                ('shedding_amount', models.IntegerField()),
                ('exercise_needs', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Dog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('age', models.IntegerField()),
                ('gender', models.CharField(max_length=20)),
                ('color', models.CharField(max_length=50)),
                ('favorite_food', models.CharField(max_length=200)),
                ('favorite_toy', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddConstraint(
            model_name='breed',
            constraint=models.CheckConstraint(check=models.Q(('size__in', ['Large', 'Small', 'Medium', 'Tiny'])), name='size'),
        ),
        migrations.AddConstraint(
            model_name='breed',
            constraint=models.CheckConstraint(check=models.Q(('friendliness__in', [1, 2, 3, 4, 5])), name='friendliness'),
        ),
        migrations.AddConstraint(
            model_name='breed',
            constraint=models.CheckConstraint(check=models.Q(('trainability__in', [1, 2, 3, 4, 5])), name='trainability'),
        ),
        migrations.AddConstraint(
            model_name='breed',
            constraint=models.CheckConstraint(check=models.Q(('shedding_amount__in', [1, 2, 3, 4, 5])), name='shedding_amount'),
        ),
        migrations.AddConstraint(
            model_name='breed',
            constraint=models.CheckConstraint(check=models.Q(('exercise_needs__in', [1, 2, 3, 4, 5])), name='exercise_needs'),
        ),
        migrations.AddField(
            model_name='dog',
            name='breed',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dogs.breed'),
        ),
    ]
