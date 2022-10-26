from rest_framework import serializers
from .models import Category, Shipper, User, Customer, Order, OrderDetail, Product
from rest_framework.fields import CurrentUserDefault


class UserSerializers(serializers.ModelSerializer):
    avatar_path = serializers.SerializerMethodField()

    def get_avatar_path(self, obj):
        request = self.context['request']
        if obj.avatar and not obj.avatar.name.startswith("/static"):
            path = '/static/%s' % obj.avatar.name

            return request.build_absolute_uri(path)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name',
                  'username', 'password', 'email',
                  'avatar', 'avatar_path', 'role']
        extra_kwargs = {
            'password': {
                'write_only': True
            }, ' avatar_path': {
                'read_only': True, 'avatar': {
                    'write_only': True
                }
            }
        }

    def create(self, validated_data):
        data = validated_data.copy()
        user = User(**data)
        user.set_password(user.password)
        user.save()
        customer = Customer(user=user)
        customer.save()
        return user


class ShipperSerializers(serializers.ModelSerializer):
    avatar_path = serializers.SerializerMethodField()

    def get_avatar_path(self, obj):
        request = self.context['request']
        if obj.avatar and not obj.avatar.name.startswith("/static"):
            path = '/static/%s' % obj.avatar.name

            return request.build_absolute_uri(path)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name',
                  'username', 'password', 'email',
                  'avatar', 'avatar_path', 'role']
        extra_kwargs = {
            'password': {
                'write_only': True
            }, ' avatar_path': {
                'read_only': True, 'avatar': {
                    'write_only': True
                }
            }
        }

    def create(self, validated_data):
        data = validated_data.copy()
        user = User(**data)
        user.set_password(user.password)
        user.role = 'Shipper'
        user.save()
        shipper = Shipper(user=user)
        shipper.save()
        return user


class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CategorySerializers(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class OrderDetailSerializers(serializers.ModelSerializer):
    product = ProductSerializers()
    sum = serializers.SerializerMethodField('get_price')

    def get_price(self, obj):
        return obj.quantity*obj.product.price

    class Meta:
        model = OrderDetail
        fields = ['order', 'product', 'quantity', 'sum', 'discount']


class CreateOrderDetailSerializers(serializers.ModelSerializer):
    sum = serializers.SerializerMethodField('get_price')

    def get_price(self, obj):
        return obj.quantity*obj.product.price

    def create(self, validated_data):
        data = validated_data.copy()
        items = OrderDetail(**data)
        print(items.product.price)
        price = items.product.price
        items.price = items.quantity*price
        items.save()

        return items

    class Meta:
        model = OrderDetail
        fields = ['order', 'product', 'quantity', 'sum', 'discount']


# class GetOrderDetailSerializers(serializers.ModelSerializer):
#     product = ProductSerializers()
#     sum = serializers.SerializerMethodField('get_price')

#     def get_price(self, obj):
#         return obj.quantity*obj.product.price

#     class Meta:
#         model = OrderDetail
#         fields = ['order', 'product', 'quantity', 'sum']


class OrderSerializers(serializers.ModelSerializer):
    item = OrderDetailSerializers(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'ship_address', 'item', 'status']
