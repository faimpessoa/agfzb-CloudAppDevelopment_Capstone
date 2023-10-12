from django.contrib import admin
from .models import CarMake, CarModel


# Register your models here.

# CarModelInline clas
#admin.site.register(CarModel)

# CarModelAdmin class
admin.site.register(CarModel)

# CarMakeAdmin class with CarModelInline
admin.site.register(CarMake)

# Register models here
