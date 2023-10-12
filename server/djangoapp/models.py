from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=200)
    #pub_date = models.DateTimeField("date created")

    def __str__(self):
        return self.name;

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object

class CarModel(models.Model):
    WAGON = 'wagon'
    SUV = 'suv'
    SEDAN = 'sedan'
    PICKUP = 'pickup'
    VEHICLETYPE_CHOICES = [
        (WAGON, 'Wagon'),
        (SUV, 'SUV'),
        (SEDAN, 'Sedan'),
        (PICKUP, 'Pick Up')
    ]
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealer = models.IntegerField(default=0)
    name = models.CharField(max_length=50)
    vehicle_type = models.CharField(
        null=False,
        max_length=20,
        choices=VEHICLETYPE_CHOICES,
        default=SUV
    )
    year = models.DateField(null=False)
    
    def __str__(self):
        return f"{self.name}, a {self.make} {self.vehicle_type}";


# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
