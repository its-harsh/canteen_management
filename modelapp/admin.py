from django.contrib import admin
from .models import Food, TotalFoodOrder, UserFoodOrder, UserOrder

# registering food model to admin site


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    pass

# registering totalfoodorder model to admin site


@admin.register(TotalFoodOrder)
class FoodAdmin(admin.ModelAdmin):
    pass

# registering userfoodorder model to admin site


@admin.register(UserFoodOrder)
class FoodAdmin(admin.ModelAdmin):
    pass

# registering userorder model to admin site


@admin.register(UserOrder)
class FoodAdmin(admin.ModelAdmin):
    pass
