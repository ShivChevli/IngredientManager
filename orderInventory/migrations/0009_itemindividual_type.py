# Generated by Django 3.2.9 on 2022-02-06 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orderInventory', '0008_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemindividual',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=models.SET(None), related_name='Item_Type', to='orderInventory.type'),
        ),
    ]
