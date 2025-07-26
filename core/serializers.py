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
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password = serializers.CharField(write_only=True)
    phone = serializers.CharField()
    email = serializers.EmailField(required=False, allow_blank=True)  # Optional field

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data.get('email', ''),  # Optional email
            password=validated_data['password'],
        )
        Customer.objects.create(
            user=user,
            phone=validated_data['phone']
        )
        return user

    def to_representation(self, instance):
        token = RefreshToken.for_user(instance)
        
        # Get related customer
        customer = Customer.objects.get(user=instance)

        return {
            "user_id": instance.id,
            "username": instance.username,
            "email": instance.email,
            "first_name": instance.first_name,
            "last_name": instance.last_name,
            "phone": customer.phone,
            "profile_image": customer.profileImage.url if customer.profileImage else None,
            "access": str(token.access_token),
            "refresh": str(token),
        }
    
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
            if customer.profileImage and hasattr(customer.profileImage, 'url'):
                data['profile_image'] = customer.profileImage.url
            else:
                data['profile_image'] = None  # or a default image URL
        except Customer.DoesNotExist:
            data['phone'] = None
            data['profile_image'] = getattr(customer, 'profileImage', None)

        data['remember_me'] = remember_me

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
    profileImage = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Customer
        fields = ['id', 'user', 'phone', 'profileImage']

    def create(self, validated_data):
        # Pop nested user data from the validated data
        user_data = validated_data.pop('user')

        # Create the user
        user = User.objects.create_user(
            username=user_data['username'],
            email=user_data.get('email', ''),
            password=user_data['password'],
            first_name=user_data.get('first_name', ''),
            last_name=user_data.get('last_name', '')
        )

        # Create the customer using the created user
        customer = Customer.objects.create(user=user, **validated_data)
        return customer

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        profile_image = validated_data.pop('profileImage', None)

        # Update customer fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Handle profile image update explicitly
        if 'profileImage' in self.initial_data:
            instance.profileImage = profile_image

            instance.save()

        # Update nested user
        user = instance.user
        for attr, value in user_data.items():
            if attr == 'password':
                user.set_password(value)
            else:
                setattr(user, attr, value)
        user.save()

        return instance

# Password Change
class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField(min_length=8)



# Address Serializer
class AddressSerializer(serializers.ModelSerializer):
    customer_id = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), source='customer', write_only=True)

    class Meta:
        model = Address
        fields = '__all__'

# Customer Address Serializer
class CustomerAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'street', 'city', 'postal_code', 'country', 'address_type', 'is_default']
        read_only_fields = ['id', 'is_default']



# Simple Models
class ImageTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageType
        fields = '__all__'

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'



# Product
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

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

# Feedback to Product
class FeedbackSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    customer_id = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), source='customer', write_only=True)
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source='product', write_only=True)

    class Meta:
        model = Feedback
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

