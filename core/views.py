from rest_framework import viewsets
from rest_framework import generics
from rest_framework.views import APIView
from .models import *
from .serializers import *

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from django.contrib.auth.models import User
from .utils import send_password_reset_email

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated

# RegisterViewSet
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer  


# JWT Login View with optional remember me
class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    

# API: Forgot Password
class ForgotPasswordView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        try:
            user = User.objects.get(email=email)
            send_password_reset_email(request, user)
            return Response({"message": "Password reset email sent."})
        except User.DoesNotExist:
            return Response({"error": "Email not found."}, status=400)

# API: Reset Password
class ResetPasswordView(APIView):
    def post(self, request, uid, token):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user_id = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(pk=user_id)
            token_generator = PasswordResetTokenGenerator()

            if not token_generator.check_token(user, token):
                return Response({"error": "Invalid or expired token."}, status=400)

            user.set_password(serializer.validated_data['password'])
            user.save()

            return Response({"message": "Password reset successful."})
        except Exception:
            return Response({"error": "Invalid link."}, status=400)


# HTML Page to serve Reset Form
def login_page(request):
    return render(request, 'test_login_jwt_&_remember_me/login_page.html')

def forgot_password_page(request):
    return render(request, 'test_login_jwt_&_remember_me/forgot_password_page.html')

def reset_password_page(request, uid, token):
    return render(request, 'test_login_jwt_&_remember_me/reset_password_page.html', {'uid': uid, 'token': token})

def home_page(request):
    return render(request, 'test_login_jwt_&_remember_me/home_page.html')

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
def editProfile(request):
    return render(request, 'aroma/editProfile.html')



# ================================================ User & Customer ====================================

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

# ================================================ Image & Menu ====================================

class ImageTypeViewSet(viewsets.ModelViewSet):
    queryset = ImageType.objects.all()
    serializer_class = ImageTypeSerializer

class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

class MenuDetailViewSet(viewsets.ModelViewSet):
    queryset = MenuDetail.objects.all()
    serializer_class = MenuDetailSerializer

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
class CustomerAddressesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        customer = request.user.customer
        addresses = customer.addresses.all()
        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data)

# ================================================ Order ====================================
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_update(self, serializer):
        serializer.save()

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

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

class BlogCommentViewSet(viewsets.ModelViewSet):
    queryset = BlogComment.objects.all()
    serializer_class = BlogCommentSerializer

class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
