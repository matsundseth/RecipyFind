from django.contrib import admin
from .models import *
from categories.models import *
# Register your models here.
admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(Amount)
admin.site.register(StoringType)
admin.site.register(Theme)
admin.site.register(Rating)
admin.site.register(Shoppinglist)

