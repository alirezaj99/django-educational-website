# Generated by Django 3.2.5 on 2021-07-30 23:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('course_app', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_paid', models.BooleanField(default=False, verbose_name='پرداخت شده/نشده؟')),
                ('payment_date', models.DateTimeField(blank=True, null=True, verbose_name='تاریخ پرداخت')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')),
                ('update', models.DateTimeField(auto_now=True, verbose_name='زمان بروزرسانی')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'سفارش',
                'verbose_name_plural': 'سفارش ها',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField()),
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
