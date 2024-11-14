from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class BusinessUser(models.Model):
    id = models.TextField(primary_key=True)
    locationId = models.ForeignKey("Location", on_delete=models.CASCADE)
    salePointId = models.ForeignKey("SalePoint", on_delete=models.CASCADE)
    
class CheersUser(models.Model):
    id = models.TextField(primary_key=True)
    displayName = models.TextField()
    phoneNumber = models.TextField(null=True, blank=True)
    
class SalePoint(models.Model):
    id = models.TextField(primary_key=True)
    locationId = models.ForeignKey("Location", on_delete=models.CASCADE)
    name = models.TextField()
    
class DrinkOrderCount(models.Model):
    count = models.IntegerField()
    drinkOrder = models.ForeignKey("DrinkOrder", on_delete=models.CASCADE)
    
class DrinkOrder(models.Model):
    bottle = models.BooleanField()
    drinkId = models.ForeignKey("Drink", on_delete=models.CASCADE)
    mixerId = models.ForeignKey("Mixer", on_delete=models.CASCADE)
    shot = models.BooleanField()
    
class Drink(models.Model):
    id = models.TextField(primary_key=True)
    name = models.TextField()
    available = models.BooleanField()
    basePrice = models.TextField()
    category = models.TextField()
    imagePath = models.TextField()
    shotPrice = models.TextField()
    currency = models.TextField()
    
class Mixer(models.Model):
    id = models.TextField(primary_key=True)
    name = models.TextField()
    available = models.BooleanField()
    imagePath = models.TextField()
    addOnPrice = models.TextField()
    
class Location(models.Model):
    id = models.TextField(primary_key=True)
    name = models.TextField()
    drinks = models.ManyToManyField("Drink")
    mixers = models.ManyToManyField("Mixer")
    imagePath = models.TextField()
    fastTrackCents = models.TextField()
    maxConsumptionCents = models.TextField()
    
class Order(models.Model):
    id = models.TextField(primary_key=True)
    amountPaidCents = models.IntegerField()
    consumerId = models.TextField()
    consumerName = models.TextField()
    drinkOrders = models.ManyToManyField("DrinkOrder")
    fastTrack = models.BooleanField()
    fcmToken = models.TextField(null=True, blank=True)
    locationId = models.ForeignKey("Location", on_delete=models.CASCADE)
    orderNumber = models.TextField()
    phoneNumber = models.TextField()
    salePointId = models.ForeignKey("SalePoint", on_delete=models.CASCADE)
    status = models.TextField()
    table = models.TextField(null=True, blank=True)
    time = models.DateTimeField()
    tip = models.TextField(null=True, blank=True)
    tipCurrency = models.TextField(null=True, blank=True)
    verificationCode = models.TextField()
    
class Music(models.Model):
    id = models.TextField(primary_key=True)
    title = models.TextField()
    albumArtURL = models.TextField()
    artistName = models.TextField()
    genres = ArrayField(models.TextField())
    locationId = models.ForeignKey("Location", on_delete=models.CASCADE)
    timestamp = models.DateTimeField()