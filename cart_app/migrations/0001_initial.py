# Generated by Django 3.2.5 on 2022-02-19 12:03

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('course_app', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('order_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')),
                ('update', models.DateTimeField(auto_now=True, verbose_name='زمان بروزرسانی')),
                ('coupon_code', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='carts', to='order_app.couponcode', verbose_name='کد تخفیف')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart', to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'سبد خرید',
                'verbose_name_plural': 'سبد های خرید',
                'ordering': ['-update'],
            },
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.PositiveIntegerField(verbose_name='قیمت')),
                ('discount', models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)], verbose_name='درصد تخفیف')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')),
                ('update', models.DateTimeField(auto_now=True, verbose_name='زمان بروزرسانی')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='cart_app.cart', verbose_name='سبد خرید')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to='course_app.course', verbose_name='دوره')),
            ],
            options={
                'verbose_name': 'ایتم سبد خرید',
                'verbose_name_plural': 'ایتم سبد خرید',
                'ordering': ['-update'],
            },
        ),
    ]
