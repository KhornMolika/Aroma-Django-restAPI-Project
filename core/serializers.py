from datetime import timedelta
import json
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.password_validation import validate_password


# Register Serializer
class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    phone = serializers.CharField()

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        customer = Customer.objects.create(user=user, phone=validated_data['phone'])
        return customer

    def to_representation(self, instance):
        return CustomerSerializer(instance).data
    
#Uses a custom token class (CustomRefreshToken) for expiry handling.
class CustomRefreshToken(RefreshToken):
    @classmethod
    def for_user_with_remember_me(cls, user, remember_me=False):
        token = cls.for_user(user)

        if remember_me:
            # Longer expiry (example: 30 days)
            token.set_exp(lifetime=timedelta(days=30))
        else:
            # Shorter expiry (example: 1 day)
            token.set_exp(lifetime=timedelta(days=1))

        return token


# Custom Token Serializer with extra data (e.g. remember me support) for Login
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    remember_me = serializers.BooleanField(default=False, write_only=True)

    def validate(self, attrs):
        # Perform default validation
        data = super().validate(attrs)
        user=self.user

        remember_me = attrs.pop('remember_me', False)

         # Issue token with dynamic expiry
        refresh = CustomRefreshToken.for_user_with_remember_me(user, remember_me)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # Add basic user info
        data.update({
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        })

        # Add phone number from Customer model if exists
        try:
            customer = Customer.objects.get(user=user)
            data['phone'] = customer.phone
        except Customer.DoesNotExist:
            data['phone'] = None

        data['remember_me'] = remember_me

        return data


# Forgot Password Serializer
class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email does not exist.")
        return value


# Reset Password Serializer
class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # write_only hides it from response
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        # Make sure to hash the password
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        return user


# Customer
class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Customer
        fields = ['id', 'user', 'phone', 'profileImage']

    def create(self, validated_data):
        # Pop nested user data from the validated data
        user_data = validated_data.pop('user')

        # Create the user
        user = User.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name']
        )

        # Create the customer using the created user
        customer = Customer.objects.create(user=user, **validated_data)
        return customer

# Simple Models
class ImageTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageType
        fields = '__all__'

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

# Product
class ProductSerializer(serializers.ModelSerializer):
    categoryID = CategorySerializer(read_only=True)
    categoryID_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='categoryID', write_only=True)

    class Meta:
        model = Product
        fields = '__all__'

class ProductDetailSerializer(serializers.ModelSerializer):
    productID = ProductSerializer(read_only=True)
    productID_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source='productID', write_only=True)

    class Meta:
        model = ProductDetail
        fields = '__all__'

# CartItem comes first to avoid circular ref
class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source='product', write_only=True)
    cart_id = serializers.PrimaryKeyRelatedField(queryset=Cart.objects.all(), source='cart', write_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'cart_id', 'product', 'product_id', 'quantity']

# Cart
class CartSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    customer_id = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), source='customer', write_only=True)
    items = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'customer', 'customer_id', 'created_at', 'items', 'total_price']

    def get_items(self, obj):
        return CartItemSerializer(obj.cartitem_set.all(), many=True).data

    def get_total_price(self, obj):
        return obj.total_price()

# QR Code
class QRCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QRCode
        fields = '__all__'


# Address Serializer
class AddressSerializer(serializers.ModelSerializer):
    customer_id = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), source='customer', write_only=True)

    class Meta:
        model = Address
        fields = ['id', 'customer_id', 'street', 'city', 'postal_code', 'country']


# OrderItem comes first to avoid circular ref
class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source='product', write_only=True)
    order_id = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all(), source='order', write_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'order_id', 'product', 'product_id', 'quantity']

# Order
class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    customer_id = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), source='customer', write_only=True)

    shipping_address = AddressSerializer(read_only=True)
    shipping_address_id = serializers.PrimaryKeyRelatedField(queryset=Address.objects.all(), source='shipping_address', write_only=True)

    payment_proof = serializers.ImageField(required=False)

    items = serializers.SerializerMethodField()
    total_amount = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id', 'customer', 'customer_id',
            'shipping_address', 'shipping_address_id',
            'order_date', 'is_paid', 'qr_invoice',
            'items', 'total_amount'
        ]

    def get_items(self, obj):
        return OrderItemSerializer(obj.orderitem_set.all(), many=True).data

    def get_total_amount(self, obj):
        return obj.total_amount()

    def create(self, validated_data):
        items_data = self.context['request'].data.get('items', [])
        items_data = json.loads(items_data) if isinstance(items_data, str) else items_data

        # Pop items key out, rest is for Order creation (QRCodeInvoice will be in validated_data as file)
        validated_data.pop('items', None)
        
        order = Order.objects.create(**validated_data)

        for item in items_data:
            OrderItem.objects.create(
                order=order,
                product_id=item.get('product_id'),
                quantity=item.get('quantity'),
                store_price=item.get('store_price'),
                product_price=item.get('product_price'),
            )

        return order


# BlogCategory
class BlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = '__all__'

# BlogDetail - REMOVE circular reference to BlogSerializer
class BlogDetailSerializer(serializers.ModelSerializer):
    blog_id = serializers.PrimaryKeyRelatedField(queryset=Blog.objects.all(), source='blog', write_only=True)

    class Meta:
        model = BlogDetail
        fields = '__all__'

# Blog
class BlogSerializer(serializers.ModelSerializer):
    category = BlogCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=BlogCategory.objects.all(), source='category', write_only=True)
    details = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = '__all__'

    def get_details(self, obj):
        details = BlogDetail.objects.filter(blog=obj).first()
        if details:
            return BlogDetailSerializer(details).data
        return None

# Blog Comment
class BlogCommentSerializer(serializers.ModelSerializer):
    blog = BlogSerializer(read_only=True)
    blog_id = serializers.PrimaryKeyRelatedField(queryset=Blog.objects.all(), source='blog', write_only=True)

    class Meta:
        model = BlogComment
        fields = '__all__'

# Feedback
class FeedbackSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    customer_id = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), source='customer', write_only=True)
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source='product', write_only=True)

    class Meta:
        model = Feedback
        fields = '__all__'
