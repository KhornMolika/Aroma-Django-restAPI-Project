from rest_framework import viewsets
from rest_framework.views import APIView

from .models import *
from .serializers import *

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from django.contrib.auth.models import User

from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated

from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from django.db import transaction
from django.core.files import File
import os
from django.conf import settings


# RegisterViewSet
class RegisterAPIView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.to_representation(user), status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

# JWT Login View with optional remember me
class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

def blog(request):
    return render(request, 'aroma/blog.html')
    
def blog_details(request, id):
    blog = get_object_or_404(Blog, id=id)
    return render(request, 'aroma/blog-Details.html', {'blog': blog})

def blogbreadcrumb_details(request, id):
    blog = get_object_or_404(Blog, id=id)
    return render(request, 'aroma/blog-Details.html', {'blog': blog})
    

# HTML Page to serve Reset Form

def blog(request):
    return render(request, 'aroma/blog.html')
def blogDetails(request):
    return render(request, 'aroma/blog-details.html')
def checkout(request):
    return render(request, 'aroma/checkout.html')
def confirmation(request):
    return render(request, 'aroma/confirmation.html')
def forgotPassword(request):
    return render(request, 'aroma/forgot-password.html')
def home(request):
    return render(request, 'aroma/index.html')
def login(request):
    return render(request, 'aroma/login.html')
def productDetail(request):
    return render(request, 'aroma/product-detail.html')
def register(request):
    return render(request, 'aroma/register.html')
def shop(request):
    return render(request, 'aroma/shop.html')
def shoppingCart(request):
    return render(request, 'aroma/shopping-cart.html')
def contact(request):
    return render(request, 'aroma/contact.html')
def account(request):
    return render(request, 'aroma/account.html')
def product_details(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'aroma/product-detail.html', {'product': product})
def productbreadcrumb_details(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'aroma/product-detail.html', {'product': product})


# ================================================ User & Customer ====================================

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    
# CustomerProfile 
class CustomerProfileViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]  # Handle image upload

    def get_object(self):
        return self.request.user.customer 

    def retrieve(self, request):
        customer = get_object_or_404(Customer, user=request.user)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    def update(self, request):
        customer = self.get_object()
        user = request.user  # Get nested user instance

        # Manually update nested user fields
        user_data_fields = ['first_name', 'last_name', 'email']
        for field in user_data_fields:
            if field in request.data:
                setattr(user, field, request.data.get(field))

        user.save()  # Save updated user

        # This ensures image is updated if included
        data = request.data.copy()
        if 'profileImage' in request.FILES:
            data['profileImage'] = request.FILES['profileImage']

        serializer = CustomerSerializer(customer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request):
        return self.update(request)
    
# Change Password
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            old_password = serializer.validated_data['old_password']
            if not user.check_password(old_password):
                return Response({"old_password": "Wrong password."}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"detail": "Password updated successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ================================================ Image & Menu ====================================

class ImageTypeViewSet(viewsets.ModelViewSet):
    queryset = ImageType.objects.all()
    serializer_class = ImageTypeSerializer

class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

# ================================================ Product ====================================

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.request.query_params.get('categoryID')
        if category_id:
            queryset = queryset.filter(categoryID_id=category_id)
        return queryset

class ProductDetailViewSet(viewsets.ModelViewSet):
    serializer_class = ProductDetailSerializer

    def get_queryset(self):
        product_id = self.request.query_params.get('productID')
        if product_id:
            return ProductDetail.objects.filter(productID_id=product_id)
        return ProductDetail.objects.all()
    
# ================================================ Cart ====================================

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

class CustomerCartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        print(f"User: {user}, Authenticated: {user.is_authenticated}")
        if not user.is_authenticated:
            raise PermissionDenied("Authentication required to view cart items.")
        return CartItem.objects.filter(cart__customer__user=user)


    def perform_create(self, serializer):
        try:
            customer = self.request.user.customer
        except Customer.DoesNotExist:
            raise PermissionDenied("No customer profile linked to user.")
        cart = Cart.objects.filter(customer=customer).first()
        if not cart:
            raise PermissionDenied("No cart found for this customer.")
        serializer.save(cart=cart)


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()

        # Only allow updating quantity (and subtotal optionally)
        quantity = request.data.get("quantity")
        if quantity is not None:
            instance.quantity = quantity
            instance.save()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)

        return Response({"error": "Quantity is required."}, status=status.HTTP_400_BAD_REQUEST)


# ================================================ QR Code ====================================

class QRCodeViewSet(viewsets.ModelViewSet):
    queryset = QRCode.objects.all()
    serializer_class = QRCodeSerializer


# ================================================ AddressViewSet ====================================

# Example endpoint to get all addresses of all customers:
class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

# Instead of requiring a customer_id in the URL, auto-fetch addresses for the logged-in customer
class CustomerAddressViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerAddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.customer.addresses.all()

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user.customer)

        @action(detail=True, methods=["post"])
        def set_default(self, request, pk=None):
            address = get_object_or_404(Address, pk=pk, customer=request.user.customer)

            Address.objects.filter(customer=request.user.customer).update(is_default=False)

            address.is_default = True
            address.save()

            return Response({"message": "Default address set successfully."}, status=status.HTTP_200_OK)


# ================================================ Order ====================================
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

class CustomerOrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            raise PermissionDenied("You must be logged in to view your orders.")
        return Order.objects.filter(customer__user=user)

    @transaction.atomic
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        user = request.user
        customer = user.customer
        shipping_address_id = request.data.get("shipping_address_id")
        is_paid = request.data.get("is_paid", False)
        items = request.data.get("items")  # JSON string
        payment_proof = request.FILES.get("payment_proof")

        # Convert is_paid from string to boolean
        if isinstance(is_paid, str):
            is_paid = is_paid.lower() == "true"

        if not shipping_address_id or not items:
            return Response({"error": "Missing shipping address or items"}, status=400)

        # Parse items JSON
        import json
        try:
            items_data = json.loads(items)
        except Exception:
            return Response({"error": "Invalid items format"}, status=400)

        # Create Order first
        order = Order.objects.create(
            customer=customer,
            shipping_address_id=shipping_address_id,
            is_paid=is_paid,
        )

        # Handle file upload from FormData
        qr_file = request.FILES.get("QRCodeInvoice", None)
        if qr_file:
            order.qr_invoice = qr_file

        if payment_proof:
            order.payment_proof = payment_proof

        # OPTIONAL: handle loading QR from saved filename
        qr_filename = request.data.get("QRCodeInvoice")  # e.g., "/media/images/qrcodes/photo.jpg"
        if qr_filename and not qr_file:
            relative_path = qr_filename.replace("/media/", "")
            full_path = os.path.join(settings.MEDIA_ROOT, relative_path)
            if os.path.exists(full_path):
                with open(full_path, "rb") as f:
                    filename = os.path.basename(full_path)
                    order.qr_invoice.save(filename, File(f), save=False)

        order.save()

        # Create OrderItems
        for item in items_data:
            OrderItem.objects.create(
                order=order,
                product_id=item.get("product_id"),
                quantity=item.get("quantity"),
                store_price=item.get("store_price", 0),
                product_price=item.get("product_price", 0),
            )

        serializer = self.get_serializer(order)
        return Response(serializer.data, status=201)


# ================================================ Blog ====================================
class BlogCategoryViewSet(viewsets.ModelViewSet):
    queryset = BlogCategory.objects.all()
    serializer_class = BlogCategorySerializer

class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

class BlogDetailViewSet(viewsets.ModelViewSet):
    queryset = BlogDetail.objects.all()
    serializer_class = BlogDetailSerializer

