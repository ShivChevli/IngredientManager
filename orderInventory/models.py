from django.db import models
from datetime import datetime
from django.core.exceptions import ValidationError
# Create your models here.


def checkMobileNumber(value):
    if len(value) != 10:
        raise ValidationError(f'{value}s must be of 10 digits')
    value = str(value)
    if not value.isnumeric():
        raise ValidationError(f'{value} must be digits')


class ItemIndividual(models.Model):
    name = models.CharField(max_length=64)
    createdAt = models.DateTimeField(default=datetime.now)
    modifyAt = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.id} : {self.name}"


class Store(models.Model):
    name = models.CharField(max_length=64)
    address = models.CharField(max_length=500, null=True, blank=True)
    emailAddress = models.EmailField(unique=True)
    mobileNumber = models.CharField(max_length=15, validators=[checkMobileNumber])

    def __str__(self):
        return f"{self.id} : {self.name} : {self.mobileNumber} : {self.address}"


class IngredientIndividual(models.Model):
    name = models.CharField(max_length=64)
    orderAt = models.ForeignKey(
        Store,
        on_delete=models.SET_NULL,
        related_name="OrderStore",
        null=True,
    )
    createdAt = models.DateTimeField(default=datetime.now)
    modifyAt = models.DateTimeField(default=None, blank=True, null=True)

    def __str__(self):
        return f"{self.id} : {self.name}"

    def json(self):
        return {
            "name" : self.name,
            "orderAt" : self.orderAt,
            "createdAt" : self.createdAt.strftime("%b %d %Y %H:%M:%S"),
            "modifyAt" : self.modifyAt,
        }



class Items(models.Model):
    itemId = models.ForeignKey(
        ItemIndividual,
        on_delete=models.CASCADE,
        related_name="itemName",
    )
    ingredientId = models.ForeignKey(
        IngredientIndividual,
        on_delete=models.CASCADE,
        related_name="ingredientName",
    )
    defaultValue = models.FloatField(null=True, blank=True)
    createdAt = models.DateTimeField(default=datetime.now)
    modifyAt = models.DateTimeField(default=None, blank=True, null=True)
    deletedAt = models.DateTimeField(default=None, blank=True, null=True)

    def __str__(self):
        return f"{self.id} : {self.itemId} : {self.ingredientId} : {self.defaultValue}"

    # def json(self):
    #     return {
    #
    #     }

class OrderIndividual(models.Model):
    name = models.CharField(max_length=64,
                            null=True, blank=True,
                            verbose_name="Name of Function For Which this order is Placed")
    mobileNumber = models.CharField(max_length=15,validators=[checkMobileNumber])
    address = models.CharField(max_length=256,blank=True,null=True)
    numberOfPerson = models.IntegerField(blank=True,null=True)
    email = models.EmailField(blank=True,null=True)
    createdAt = models.DateTimeField(default=datetime.now)
    deliveredAt = models.DateTimeField(blank=True, null=True)
    deletedAt = models.DateTimeField(default=None, blank=True, null=True)

    def __str__(self):
        return f"{self.id} : {self.name}"


class Order(models.Model):
    orderId = models.ForeignKey(
        OrderIndividual,
        related_name="orderName",
        on_delete=models.CASCADE,
        verbose_name="To track Order",
    )
    itemId = models.ForeignKey(
        Items,
        related_name="ItemName",
        on_delete=models.CASCADE,
        verbose_name="Items With Ingredient Which need to Order",
    )
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.id} : {self.orderId} : {self.itemId.itemId.name} : {self.itemId.ingredientId.name} : {self.quantity}"
