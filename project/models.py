from django.db import models
from django.contrib.postgres.fields import ArrayField
#import pyrebase
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os
from google.cloud.firestore import FieldFilter

cred = credentials.Certificate("cheers-460f2-fd5e3013b68e.json")
# TODO: ENABLE CRUD FOR DJANGO OBJECTS
# only load data once so that 
# deletions/modifications can persist through refreshes/restarts

firebase_admin.initialize_app(cred)

db = firestore.client()

load_dotenv()

API_KEY=os.getenv("API_KEY")

config = {
  "apiKey": API_KEY,
  "authDomain": "cheers-460f2.firebaseapp.com",
  "projectId": "cheers-460f2",
  "storageBucket": "cheers-460f2.appspot.com",
  "appId": "1:765440259273:web:0925849297ff916903c918",
  "measurementId": "G-MT2B0WJN6E"
}

#firebase = pyrebase.initialize_app(config)

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
    # add location id?
    
    def __str__(self):
        return f"{self.name}, category: {self.category}, id: {self.id}"
    
class Mixer(models.Model):
    id = models.TextField(primary_key=True)
    name = models.TextField()
    available = models.BooleanField()
    imagePath = models.TextField()
    addOnPrice = models.TextField()
    
    def __str__(self):
        return f"{self.name}, id: {self.id}"
    
class Location(models.Model):
    #MUST BE STANDALONE, NO FOREIGN KEYS, TO MEET PROJECT REQUIREMENTS
    id = models.TextField(primary_key=True)
    name = models.TextField()
    drinks = models.ManyToManyField("Drink")
    mixers = models.ManyToManyField("Mixer")
    imagePath = models.TextField()
    fastTrackCents = models.TextField()
    maxConsumptionCents = models.TextField()
    
    def __str__(self):
        return f"{self.name}, id: {self.id}"
    
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
    consumptionOrder = models.BooleanField(blank=True, null=True) #can be null
    
class Music(models.Model):
    id = models.TextField(primary_key=True)
    title = models.TextField()
    albumArtURL = models.TextField()
    artistName = models.TextField()
    genres = models.TextField() #string of genres separated by , use .split(',') and .strip() to get list
    locationId = models.TextField()
    timestamp = models.DateTimeField()
    
    def __str__(self):
        return f"{self.title}, artist: {self.artistName}, id: {self.id}"
    
    
def locationData():
    # CHANGE TO GET LOCATION ID FROM LOGGED IN USER
    result = db.collection('locations_v2').document("LlnX4nPSdFPlnyckEJiR").get().to_dict()
    print(result)
    return result

def musicData():
     # CHANGE TO GET LOCATION ID FROM LOGGED IN USER
    result = db.collection('music').where(filter=FieldFilter("locationId", "==", "LlnX4nPSdFPlnyckEJiR")).get()
    #convert to dict
    result = {doc.id: doc.to_dict() for doc in result}
    print(result)
    return result

def load_data():
    
    # make exception for duplicates, name or id, possible problem with orders
    
    location_data = locationData()
    
    for k, d in location_data.get('drinks', {}).items():
        drink_id = k
        name = d.get('name')
        available = d.get('available', False)
        basePrice = d.get('basePrice')
        category = d.get('category')
        imagePath = d.get('imagePath')
        shotPrice = d.get('shotPrice', '')
        currency = d.get('currency')
        
        #create drink if id doesn't exist, and set defaults
        drink, created = Drink.objects.get_or_create(
            id=drink_id,
            defaults={
                'name': name,
                'available': available,
                'basePrice': basePrice,
                'category': category,
                'imagePath': imagePath,
                'shotPrice': shotPrice,
                'currency': currency
            }
        )
        
        #if we didn't create the drink, we can update the fields
        if not created:
            drink.name = name
            drink.available = available
            drink.basePrice = basePrice
            drink.category = category
            drink.imagePath = imagePath
            drink.shotPrice = shotPrice
            drink.currency = currency
            drink.save()
            
    for k, m in location_data.get('mixers', {}).items():
        mixer_id = k
        name = m.get('name')
        available = m.get('available')
        imagePath = m.get('imagePath')
        addOnPrice = m.get('addOnPrice')
        
        #create mixer if id doesn't exist, and set defaults
        mixer, created = Mixer.objects.get_or_create(
            id=mixer_id,
            defaults={
                'name': name,
                'available': available,
                'imagePath': imagePath,
                'addOnPrice': addOnPrice
            }
        )
        
        #if we didn't create the mixer, we can update the fields
        if not created:
            mixer.name = name
            mixer.available = available
            mixer.imagePath = imagePath
            mixer.addOnPrice = addOnPrice
            mixer.save()
            
    
    # CHANGE TO GET LOCATION ID FROM LOGGED IN BUSINESS USER
    location_id = 'LlnX4nPSdFPlnyckEJiR'
        
    #create location if id doesn't exist, and set defaults
    location, created = Location.objects.get_or_create(
        id=location_id,
        defaults={
            'name': location_data.get('name'),
            'imagePath': location_data.get('imagePath'),
            'fastTrackCents': location_data.get('fastTrackCents'),
            'maxConsumptionCents': location_data.get('maxConsumptionCents')
        }
    )
    
    #if we didn't create the location, we can update the fields
    if not created:
        location.name = location_data.get('name')
        location.imagePath = location_data.get('imagePath')
        location.fastTrackCents = location_data.get('fastTrackCents')
        location.maxConsumptionCents = location_data.get('maxConsumptionCents')
        location.save()
        
    # adding the drinks to the ManytoMany field of the Location
    for k in location_data.get('drinks', {}).keys():
        location.drinks.add(Drink.objects.get(id=k))
    
    # adding the mixers to the ManytoMany field of the Location
    for k in location_data.get('mixers', {}).keys():
        location.mixers.add(Mixer.objects.get(id=k))
    location.save()
    
    music_data = musicData()
    
    for k, m in music_data.items():
        music_id = k
        title = m.get('title')
        print(f'title: {title}')
        albumArtURL = m.get('albumArtURL')
        print(f'albumArtURL: {albumArtURL}')
        artistName = m.get('artistName')
        print(f'artistName: {artistName}')
        genres = ', '.join(m.get('genres'))
        print(f'genres: {genres}')
        timestamp = m.get('timestamp')
        print(f'timestamp: {timestamp}')
        locationId = m.get('locationId')
        print(f'locationId: {locationId}')
        print('----------------')
        
        #create music if id doesn't exist, and set defaults
        music, created = Music.objects.get_or_create(
            id=music_id,
            defaults={
                'title': title,
                'albumArtURL': albumArtURL,
                'artistName': artistName,
                'genres': genres,
                'timestamp': timestamp,
                'locationId': locationId
            }
        )
        
        #if we didn't create the music, we can update the fields
        if not created:
            music.title = title
            music.albumArtURL = albumArtURL
            music.artistName = artistName
            music.genres = genres
            music.timestamp = timestamp
            music.locationId = locationId
            music.save()
        
   
