# Generated by Django 5.0.6 on 2024-06-27 19:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beats', '0018_alter_beats_audio_file'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lu', models.BooleanField(default=False)),
                ('position', models.IntegerField(default=0)),
                ('beat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='beats.beats')),
                ('utilisateur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
