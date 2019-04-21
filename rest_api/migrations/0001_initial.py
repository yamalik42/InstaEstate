# Generated by Django 2.2 on 2019-04-14 19:49

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('first_name', models.CharField(max_length=21, validators=[django.core.validators.RegexValidator('^[A-Za-z]+$')])),
                ('last_name', models.CharField(max_length=21, validators=[django.core.validators.RegexValidator('^[A-Za-z]+$')])),
                ('phone', models.CharField(max_length=10, validators=[django.core.validators.RegexValidator('^[0-9]{10}$')])),
                ('seller', models.BooleanField(default=False)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('description', models.TextField(max_length=642)),
                ('image', models.ImageField(default='default_user/default_user.jpg', upload_to='users/')),
            ],
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=21)),
                ('address', models.CharField(max_length=21)),
                ('city', models.CharField(max_length=21)),
                ('state', models.CharField(max_length=21)),
                ('zip_code', models.CharField(max_length=21, validators=[django.core.validators.RegexValidator('^[0-9]{6}$')])),
                ('price', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('bedroom', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('bathroom', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('square_feet', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('lot_size', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('garage', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('listing_date', models.DateField(auto_now_add=True)),
                ('description', models.TextField(max_length=442)),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PropertyImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='properties/')),
                ('estate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rest_api.Property')),
            ],
        ),
        migrations.CreateModel(
            name='Inquiry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(max_length=442)),
                ('sent_date', models.DateField(auto_now_add=True)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('estate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rest_api.Property')),
            ],
        ),
    ]
