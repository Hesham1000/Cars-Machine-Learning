# Generated by Django 4.0.5 on 2022-07-10 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='register',
            name='password',
            field=models.CharField(help_text='please enter password', max_length=50, unique=True),
        ),
    ]
