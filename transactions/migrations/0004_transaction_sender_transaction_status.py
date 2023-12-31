# Generated by Django 4.2.3 on 2023-07-06 16:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('transactions', '0003_alter_cryptocurrency_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='sender',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Sender User'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transaction',
            name='status',
            field=models.CharField(choices=[('PROCESSING', 'Processing'), ('CANCELED', 'Canceled'), ('ACCEPTED', 'Accepted')], default='PROCESSING', editable=False, max_length=10, verbose_name='Transaction status'),
            preserve_default=False,
        ),
    ]
