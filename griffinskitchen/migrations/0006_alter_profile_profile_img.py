# Generated by Django 4.1.1 on 2022-12-03 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('griffinskitchen', '0005_alter_profile_profile_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_img',
            field=models.ImageField(default='blank-profile-picture.png', upload_to='profile_images'),
        ),
    ]
