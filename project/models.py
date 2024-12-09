# File: project/models.py
# Author: Jose Maria Amusategui Garcia Peri (jmamus@bu.edu) 13/11/2024
# Description: Defines the models for the the project app. Some of the models may seem 
# unnecessarily complicated, but the original DB is non-relational, making this all the more difficult.

from django.db import models
from django.contrib.postgres.fields import ArrayField
#import pyrebase
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os
from google.cloud.firestore import FieldFilter
import json
from django.contrib.auth.models import User
from django.urls import reverse

load_dotenv()
# Cannot upload the json file to Heroku, so we need to get 
# the credentials from the environment
#cred = credentials.Certificate("cheers-460f2-fd5e3013b68e.json")

jsonCreds = os.environ.get("GOOGLE_CREDS", "{}")
dictCreds = json.loads(jsonCreds)
cred = credentials.Certificate(dictCreds)

# only load data once so that 
# deletions/modifications can persist through refreshes/restarts

firebase_admin.initialize_app(cred)

db = firestore.client()



#firebase = pyrebase.initialize_app(config)

# Create your models here.
class BusinessUser(models.Model):
    '''Store Business User information.'''
    id = models.TextField(primary_key=True)
    locationId = models.ForeignKey("Location", on_delete=models.CASCADE)
    #may need to change in future to allow for multiple sale points, now only one per user
    salePointId = models.ForeignKey("SalePoint", on_delete=models.CASCADE)
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    def getLocationId(self):
        '''Return the location id of this BusinessUser.'''
        return self.locationId
    
    def __str__(self):
        '''Return a string representation of this BusinessUser Object.'''
        return f"id: {self.id}, location: {self.locationId}, salePoint: {self.salePointId}"
    
class CheersUser(models.Model):
    '''Store information of Cheers! users collection docs.'''
    id = models.TextField(primary_key=True)
    displayName = models.TextField(null=True, blank=True)
    phoneNumber = models.TextField(null=True, blank=True)
    
    def __str__(self):
        '''Return a string representation of this CheersUser Object.'''
        return f"{self.displayName}, id: {self.id}, phoneNumber: {self.phoneNumber}"
    
class SalePoint(models.Model):
    '''Store Sale Point information.'''
    id = models.TextField(primary_key=True)
    locationId = models.ForeignKey("Location", on_delete=models.CASCADE)
    name = models.TextField()
    
    def __str__(self):
        '''Return a string representation of this SalePoint Object.'''
        return f"{self.name}, id: {self.id}, location: {self.locationId}"
    
class DrinkOrderCount(models.Model):
    '''Store Drink Order Count information, used to make up DrinkOrderCounts as part of an Order.'''
    count = models.IntegerField()
    drinkOrder = models.ForeignKey("DrinkOrder", on_delete=models.CASCADE)
    
    def __str__(self):
        '''Return a string representation of this DrinkOrderCount Object.'''
        return f"count: {self.count}, drinkOrder: {self.drinkOrder}"
    
class DrinkOrder(models.Model):
    '''Store Drink Order information, used to set drink details for a DrinkOrderCount.'''
    bottle = models.BooleanField()
    drinkId = models.ForeignKey("Drink", on_delete=models.CASCADE, null=True, blank=True) #can be null and not required
    mixerId = models.ForeignKey("Mixer", on_delete=models.CASCADE, null=True, blank=True) #can be null and not required
    shot = models.BooleanField()
    
    def __str__(self):
        '''Return a string representation of this DrinkOrder Object.'''
        return f"bottle: {self.bottle}, drink: {self.drinkId}, mixer: {self.mixerId}, shot: {self.shot}"
    
class Drink(models.Model):
    '''Store Drink information.'''
    id = models.TextField(primary_key=True)
    name = models.TextField()
    available = models.BooleanField()
    basePrice = models.TextField()
    category = models.TextField()
    imagePath = models.TextField()
    shotPrice = models.TextField()
    currency = models.TextField()
    # add location id maybe?
    
    def __str__(self):
        '''Return a string representation of this Drink Object.'''
        return f"{self.name}, category: {self.category}, id: {self.id}"
    
class Mixer(models.Model):
    '''Store Mixer information.'''
    id = models.TextField(primary_key=True)
    name = models.TextField()
    available = models.BooleanField()
    imagePath = models.TextField()
    addOnPrice = models.TextField()
    
    def __str__(self):
        '''Return a string representation of this Mixer Object.'''
        return f"{self.name}, id: {self.id}"
    
class Location(models.Model):
    '''Store Location information.'''
    #MUST BE STANDALONE, NO FOREIGN KEYS, TO MEET PROJECT REQUIREMENTS
    id = models.TextField(primary_key=True)
    name = models.TextField()
    drinks = models.ManyToManyField("Drink")
    mixers = models.ManyToManyField("Mixer")
    imagePath = models.TextField()
    fastTrackCents = models.TextField()
    maxConsumptionCents = models.TextField()
    
    def __str__(self):
        '''Return a string representation of this Location Object.'''
        return f"{self.name}, id: {self.id}"
    
class Order(models.Model):
    '''Store Order information.'''
    id = models.TextField(primary_key=True)
    amountPaidCents = models.IntegerField()
    consumerId = models.TextField()
    consumerName = models.TextField()
    drinkOrderCounts = models.ManyToManyField("DrinkOrderCount") #A django admin glitch 
    # shows tons of duplicates/other objects, 
    # checked with ORM and all good though, this drove me absolutely crazy
    fastTrack = models.BooleanField()
    fcmToken = models.TextField(null=True, blank=True)
    locationId = models.ForeignKey("Location", on_delete=models.CASCADE)
    orderNumber = models.TextField()
    phoneNumber = models.TextField(blank=True, null=True) #can be null
    salePointId = models.ForeignKey("SalePoint", on_delete=models.CASCADE)
    status = models.TextField()
    table = models.TextField(null=True, blank=True)
    time = models.DateTimeField()
    tip = models.TextField(null=True, blank=True)
    tipCurrency = models.TextField(null=True, blank=True)
    verificationCode = models.TextField()
    consumptionOrder = models.BooleanField(blank=True, null=True) #can be null
    
    def __str__(self):
        '''Return a string representation of this Order Object.'''
        return f"consumer: {self.consumerName}, id: {self.id}, status: {self.status}, verificationCode: {self.verificationCode}"
    
class Music(models.Model):
    '''Store Music information.'''
    id = models.TextField(primary_key=True, editable=False)
    title = models.TextField()
    albumArtURL = models.TextField()
    artistName = models.TextField()
    genres = models.TextField() # saved as json string using 
    # json.dumps(array), can be converted back to array using json.loads(string) 
    locationId = models.TextField()
    timestamp = models.DateTimeField()
    
    def __str__(self):
        '''Return a string representation of this Music Object.'''
        return f"{self.title}, artist: {self.artistName}, id: {self.id}"
    
    def get_absolute_url(self):
        return reverse("musicDetail", kwargs={"pk": self.pk})
    
    
    
def locationData():
    '''Get location data for a specific location from Firestore collection locations_v2.'''
    # May need to change to get location id from logged in user, for now there is only one
    # location in the Firestore collection
    result = db.collection('locations_v2').document("LlnX4nPSdFPlnyckEJiR").get().to_dict()
    #print(result)
    return result

def musicData():
    '''Get music data for a specific location from Firestore collection music.'''
    # May need to change to get location id from logged in user, for now there is only one
    # location in the Firestore collection
    result = db.collection('music').where(filter=FieldFilter("locationId", "==", "LlnX4nPSdFPlnyckEJiR")).get()
    #convert to dict
    result = {doc.id: doc.to_dict() for doc in result}
    #print(result)
    return result

def ordersData():
    '''Get orders data for a specific location from Firestore collection orders_v2.'''
    # May need to change to get location id from logged in user, for now there is only one
    # location in the Firestore collection
    result = db.collection('orders_v2').where(filter=FieldFilter("locationId", "==", "LlnX4nPSdFPlnyckEJiR")).get()
    #convert to dict
    result = {doc.id: doc.to_dict() for doc in result}
    #print(result)
    return result

def salePointsData():
    '''Get sale points data for a specific location from Firestore collection salePoints.'''
    # May need to change to get location id from logged in user, for now there is only one
    # location in the Firestore collection
    result = db.collection('salePoints').where(filter=FieldFilter("locationId", "==", "LlnX4nPSdFPlnyckEJiR")).get()
    #convert to dict
    result = {doc.id: doc.to_dict() for doc in result}
    #print(result)
    return result

def businessUsersData():
    '''Get business users data for a specific location from Firestore collection businessUsers.'''
    # May need to change to get location id from logged in user, for now there is only one
    # location in the Firestore collection
    result = db.collection('businessUsers').where(filter=FieldFilter("locationId", "==", "LlnX4nPSdFPlnyckEJiR")).get()
    #convert to dict
    result = {doc.id: doc.to_dict() for doc in result}
    #print(result)
    return result

def cheersUsersData():
    '''Get cheers users data from Firestore collection users.'''
    result = db.collection('users').get()
    #convert to dict
    result = {doc.id: doc.to_dict() for doc in result}
    #print(result)
    return result




def load_data():
    '''Load data from Firestore into Django models. 
    While it may seem unnecessarily large/complicated, 
    we are essentially transforming a non-relational DB into a relational one.'''
    
    # possibly make exception for duplicates, name or id, possible problem with orders
    
    location_data = locationData()
    # Retrieve all drinks from the location data
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
            
    # Retrieve all mixers from the location data        
    for k, m in location_data.get('mixers', {}).items():
        mixer_id = k
        name = m.get('name')
        available = m.get('available')
        imagePath = m.get('imagePath')
        addOnPrice = m.get('addOnPrice')
        
        #create mixer if id doesn't exist, and set defaults
        # look into update_or_create
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
            
    
    # May need to change to get location id from logged in user, for now there is only one
    # location in the Firestore collection
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
    
    # Retrieve all music from the music data
    for k, m in music_data.items():
        music_id = k
        title = m.get('title')
        #print(f'title: {title}')
        albumArtURL = m.get('albumArtURL')
        #print(f'albumArtURL: {albumArtURL}')
        artistName = m.get('artistName')
        #print(f'artistName: {artistName}')
        genres = json.dumps(m.get('genres'))
        #print(f'genres: {genres}')
        timestamp = m.get('timestamp')
        #print(f'timestamp: {timestamp}')
        locationId = m.get('locationId')
        #print(f'locationId: {locationId}')
        #print('----------------')
        
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
            
            
    sale_points_data = salePointsData()
    
    # Retrieve all sale points from the sale points data
    for k, s in sale_points_data.items():
        sale_point_id = k
        name = s.get('name')
        locationId = s.get('locationId')
        
        #create sale point if id doesn't exist, and set defaults
        sale_point, created = SalePoint.objects.get_or_create(
            id=sale_point_id,
            defaults={
                'name': name,
                'locationId': Location.objects.get(id=locationId)
            }
        )
        
        #if we didn't create the sale point, we can update the fields
        if not created:
            sale_point.name = name
            sale_point.locationId = Location.objects.get(id=locationId)
            sale_point.save()
    
    
    orders_data = ordersData()
    # Delete all Orders, DrinkOrderCount, and DrinkOrder before loading new ones to avoid duplicates
    Order.objects.all().delete()
    DrinkOrderCount.objects.all().delete()
    DrinkOrder.objects.all().delete()
    
    # Retrieve all orders from the orders data
    for k, o in orders_data.items():
        order_id = k
        amountPaidCents = o.get('amountPaidCents')
        consumerId = o.get('consumerId')
        consumerName = o.get('consumerName')
        fastTrack = o.get('fastTrack')
        fcmToken = o.get('fcmToken')
        orderNumber = o.get('orderNumber')
        phoneNumber = o.get('phoneNumber')
        status = o.get('status')
        table = o.get('table')
        time = o.get('time')
        tip = o.get('tip')
        tipCurrency = o.get('tipCurrency')
        verificationCode = o.get('verificationCode')
        consumptionOrder = o.get('consumptionOrder')
        
        # Foreign keys
        locationId = Location.objects.get(id=o.get('locationId'))
        salePointId = SalePoint.objects.get(id=o.get('salePointId'))
        
        #many to many field for drinkOrderCounts
        drinkOrderCounts = o.get('drinkOrderCounts')
        #print(f'drinkOrderCounts: {drinkOrderCounts}')
        
        drinkOrderCountsList = []
        # loop through drinkOrderCounts to create DrinkOrder and DrinkOrderCount objects
        # for this order
        for d in drinkOrderCounts:
            #print(f'd: {d}')
            count = d.get('count')
            #print(f'count: {count}')
            drinkOrder = d.get('drinkOrder')
            #print(f'drinkOrder: {drinkOrder}')
            drinkOrderMixerId = drinkOrder.get('mixerId')
            #print(f'drinkOrderMixerId: {drinkOrderMixerId}')
            drinkOrderDrinkId = drinkOrder.get('drinkId')
            #print(f'drinkOrderDrinkId: {drinkOrderDrinkId}')
            drinkOrderBottle = drinkOrder.get('bottle')
            #print(f'drinkOrderBottle: {drinkOrderBottle}')
            drinkOrderShot = drinkOrder.get('shot')
            #print(f'drinkOrderShot: {drinkOrderShot}')
            
            if drinkOrderDrinkId != "":
                drink = Drink.objects.get(id=drinkOrderDrinkId)
            else:
                drink = None
                
            if drinkOrderMixerId != "":
                mixer = Mixer.objects.get(id=drinkOrderMixerId)
            else:
                mixer = None
                
            # create DrinkOrder object
            drinkOrderFinal = DrinkOrder(
                bottle = drinkOrderBottle,
                drinkId = drink,
                mixerId = mixer,
                shot = drinkOrderShot
            )
            drinkOrderFinal.save()
            
            # create DrinkOrderCount object
            drinkOrderCountFinal = DrinkOrderCount(
                count = count,
                drinkOrder = DrinkOrder.objects.get(pk=drinkOrderFinal.pk)
            )
            drinkOrderCountFinal.save()
            
            drinkOrderCountsList.append(drinkOrderCountFinal)
            
        # finally create the Order object without the drinkOrderCounts
        order = Order(
            id = order_id,
            amountPaidCents = amountPaidCents,
            consumerId = consumerId,
            consumerName = consumerName,
            fastTrack = fastTrack,
            fcmToken = fcmToken,
            locationId = locationId,
            orderNumber = orderNumber,
            phoneNumber = phoneNumber,
            salePointId = salePointId,
            status = status,
            table = table,
            time = time,
            tip = tip,
            tipCurrency = tipCurrency,
            verificationCode = verificationCode,
            consumptionOrder = consumptionOrder
        )
        order.save()
            
        
        #print(f'drinkOrderCountsList: {drinkOrderCountsList}')
        
        # Clear the many to many field, just in case
        order.drinkOrderCounts.clear()
        # Iterate through the list of drinkOrderCounts and add them to the order
        for d in drinkOrderCountsList:
            #print(f'drinkOrderCount: {d}')
            #print(f'd.pk: {d.pk}')
            order.drinkOrderCounts.add(DrinkOrderCount.objects.get(pk=d.pk))
        order.save()
        
        
        business_data = businessUsersData()
        
        # Retrieve all business users from the business data
        for k, b in business_data.items():
            business_id = k
            locationId = b.get('locationId')
            salePointId = b.get('salePointId')
            
            #create business user if id doesn't exist, and set defaults
            business_user, created = BusinessUser.objects.get_or_create(
                id=business_id,
                defaults={
                    'locationId': Location.objects.get(id=locationId),
                    'salePointId': SalePoint.objects.get(id=salePointId)
                }
            )
            
            #if we didn't create the business user, we can update the fields
            if not created:
                business_user.locationId = Location.objects.get(id=locationId)
                business_user.salePointId = SalePoint.objects.get(id=salePointId)
                business_user.save()
                
        
        users_data = cheersUsersData()
        
        # Retrieve all cheers users from the users data
        for k, u in users_data.items():
            user_id = k
            
            if 'displayName' in u:
                displayName = u.get('displayName')
            else:
                displayName = None
            
            if 'phoneNumber' in u:
                phoneNumber = u.get('phoneNumber')
            else:
                phoneNumber = None
                 
            
            #create cheers user if id doesn't exist, and set defaults
            cheers_user, created = CheersUser.objects.get_or_create(
                id=user_id,
                defaults={
                    'displayName': displayName,
                    'phoneNumber': phoneNumber
                }
            )
            
            #if we didn't create the cheers user, we can update the fields
            if not created:
                cheers_user.displayName = displayName
                cheers_user.phoneNumber = phoneNumber
                cheers_user.save()
                
def deleteAll():
    '''Delete all data from all models.'''
    # Useful for debugging and testing
    BusinessUser.objects.all().delete()
    CheersUser.objects.all().delete()
    SalePoint.objects.all().delete()
    DrinkOrderCount.objects.all().delete()
    DrinkOrder.objects.all().delete()
    Drink.objects.all().delete()
    Mixer.objects.all().delete()
    Location.objects.all().delete()
    Order.objects.all().delete()
    Music.objects.all().delete()