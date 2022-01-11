# Generated by Django 3.2.9 on 2022-01-11 12:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orderInventory', '0006_auto_20220109_1335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='orderItem',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ItemName', to='orderInventory.itemindividual', verbose_name='Items With Ingredient Which need to Order'),
        ),
    ]