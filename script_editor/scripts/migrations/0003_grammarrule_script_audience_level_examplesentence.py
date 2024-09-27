# Generated by Django 5.1 on 2024-09-16 06:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scripts', '0002_script_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='GrammarRule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='script',
            name='audience_level',
            field=models.CharField(default='general', max_length=50),
        ),
        migrations.CreateModel(
            name='ExampleSentence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('incorrect_sentence', models.TextField()),
                ('corrected_sentence', models.TextField()),
                ('rule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='examples', to='scripts.grammarrule')),
            ],
        ),
    ]
