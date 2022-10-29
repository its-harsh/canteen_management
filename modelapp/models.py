from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()  # this function returns user model of site


class Food(models.Model):
    # there is all food details that is to be stored by database
    food_name = models.CharField(verbose_name='Food Name', max_length=255)
    food_price = models.FloatField(verbose_name='Price ($)')
    food_type = models.CharField(verbose_name='Type', max_length=255)
    food_content = models.CharField(verbose_name='Ingredients', max_length=255)
    veg_or_non = models.BooleanField(verbose_name='Vegeterian', default=False)
    discount = models.IntegerField(verbose_name='Discount (%)', default=0)
    tax = models.IntegerField(
        verbose_name='Tax (%)', default=5
    )

    def __str__(self):
        return self.food_name


class TotalFoodOrder(models.Model):
    # there is all details of total food ordered and to be prepared by chef with name
    food = models.OneToOneField(Food, on_delete=models.CASCADE)
    no_of_orders = models.IntegerField(
        verbose_name='No of Orders for this food', default=0
    )

    def __str__(self):
        return self.food.__str__()


class UserFoodOrder(models.Model):
    # this model sotres the name of food and no of entity orderd by a user in a order of diffrent objects
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    count = models.IntegerField(verbose_name='Count', default=0)
    delivered = models.BooleanField(verbose_name='Delivered', default=False)

    def __str__(self):
        return self.food.__str__()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # oveeriding save method so that when this model saves the total food order count can
        # be updated
        try:
            total_food_order = TotalFoodOrder.objects.get(food=self.food)
        except TotalFoodOrder.DoesNotExist:
            total_food_order = TotalFoodOrder.objects.create(food=self.food)
        if not self.delivered:
            total_food_order.no_of_orders += self.count
            total_food_order.save()
        return super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)


class UserOrder(models.Model):
    # this stores the data of particular order
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, limit_choices_to={
            'groups__name': 'Buyers'
        }
    )
    food_orders = models.ManyToManyField(UserFoodOrder)
    delivered = models.BooleanField(verbose_name='Delivered', default=False)

    def __str__(self):
        return self.user.__str__()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # ovveriding the save method so that this is delivered every instance related to this instance
        # is mentioned dilivered status
        if self.delivered:
            for i in self.food_orders.all():
                i.delivered = True
                totalfoodorder = i.food.totalfoodorder
                totalfoodorder.no_of_orders -= i.count
                totalfoodorder.save()
                i.save()
        return super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
