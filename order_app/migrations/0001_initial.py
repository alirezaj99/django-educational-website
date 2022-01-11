# Generated by Django 3.2.5 on 2022-01-11 21:03

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('course_app', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CouponCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, unique=True, verbose_name='کد تخفیف')),
                ('discount', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)], verbose_name='درصد تخفیف')),
                ('start', models.DateTimeField(default=django.utils.timezone.now, verbose_name='زمان شروع')),
                ('end', models.DateTimeField(verbose_name='زمان پایان')),
                ('status', models.BooleanField(default=True, verbose_name='فعال / غیرفعال؟')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')),
                ('update', models.DateTimeField(auto_now=True, verbose_name='زمان بروزرسانی')),
            ],
            options={
                'verbose_name': 'کد تخفیف',
                'verbose_name_plural': 'کد های تخفیف',
                'ordering': ['-status', '-created'],
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('w', 'waiting'), ('s', 'success'), ('f', 'failed')], default='w', max_length=1)),
                ('is_free', models.BooleanField(default=False, verbose_name='رایگان؟')),
                ('payment_date', models.DateTimeField(blank=True, null=True, verbose_name='تاریخ پرداخت')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')),
                ('update', models.DateTimeField(auto_now=True, verbose_name='زمان بروزرسانی')),
                ('coupon_code', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='order_app.couponcode', verbose_name='کد تخفیف')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'سفارش',
                'verbose_name_plural': 'سفارش ها',
                'ordering': ['-payment_date', '-created'],
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.PositiveIntegerField(verbose_name='قیمت')),
                ('discount', models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)], verbose_name='درصد تخفیف')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')),
                ('update', models.DateTimeField(auto_now=True, verbose_name='زمان بروزرسانی')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='course_app.course', verbose_name='دوره')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='order_app.order', verbose_name='سفارش')),
            ],
            options={
                'verbose_name': 'آیتم سفارش',
                'verbose_name_plural': 'آیتم های سفارش',
                'ordering': ['-created'],
            },
        ),
    ]
