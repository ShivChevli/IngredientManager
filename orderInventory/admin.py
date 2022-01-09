from django.contrib import admin

from . import models
# Register your models here.

admin.site.register(models.Category)
admin.site.register(models.Order)
admin.site.register(models.OrderIndividual)
admin.site.register(models.Items)
admin.site.register(models.ItemIndividual)
admin.site.register(models.IngredientIndividual)