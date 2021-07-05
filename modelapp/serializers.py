from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Food, TotalFoodOrder, UserFoodOrder, UserOrder


User = get_user_model()

# serializing data of all food items


class ListFoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = '__all__'

# serializing some data of food object


class GetFoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ['id', 'food_name', 'food_price',
                  'veg_or_non', 'discount', 'tax']

# serializing some properties of user model


class GetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

# serializing user food order model for get method


class GetUserFoodOrderSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    food = GetFoodSerializer()
    count = serializers.IntegerField()

# serializing user food order model for create method


class CreateUserFoodOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFoodOrder
        exclude = ['delivered']

# serializing food order by user


class GetUserOrderSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    user = GetUserSerializer()
    food_orders = GetUserFoodOrderSerializer(many=True)
    delivered = serializers.BooleanField()


class CreateUserOrderSerializer(serializers.ModelSerializer):
    food_orders = CreateUserFoodOrderSerializer(many=True)

    class Meta:
        model = UserOrder
        fields = '__all__'

    def create(self, validated_data):
        user_food_order_list = validated_data.pop('food_orders')
        instance = UserOrder.objects.create(**validated_data)
        print(validated_data)
        print(user_food_order_list)
        for i in user_food_order_list:
            user_food_order = UserFoodOrder.objects.create(**i)
            instance.food_orders.add(user_food_order.id)
        return instance
