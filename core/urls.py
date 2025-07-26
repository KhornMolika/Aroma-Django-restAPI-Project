from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import *
from core import views

# DRF Router for ViewSets
router = DefaultRouter()

# User and Customer
router.register(r'users', UserViewSet, basename='user')
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'addresses', AddressViewSet, basename='addresses')
router.register(r'customer-addresses', CustomerAddressViewSet, basename='customer-addresses')

# Image-related
router.register(r'image-types', ImageTypeViewSet, basename='imagetype')
router.register(r'images', ImageViewSet, basename='image')

# Product and Category
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'product-details', ProductDetailViewSet, basename='productdetail')

# Feedback
router.register(r'feedbacks', FeedbackViewSet, basename='feedback')

# Cart and Order
router.register(r'cart-items', CartItemViewSet, basename='cartitem')
router.register(r'carts', CartViewSet, basename='cart')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'order-items', OrderItemViewSet, basename='orderitem')

# QR Code
router.register(r'qrcodes', QRCodeViewSet, basename='qrcode')

# Blog
router.register(r'blog-categories', BlogCategoryViewSet, basename='blogcategory')
router.register(r'blogs', BlogViewSet, basename='blog')
router.register(r'blog-details', BlogDetailViewSet, basename='blogdetail')
router.register(r'blog-comments', BlogCommentViewSet, basename='blogcomment')

# Custom view for Customer Profile
customer_profile = CustomerProfileViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
})

urlpatterns = [
    # API Auth
    path('api/register/', RegisterAPIView.as_view(), name='register'),
    path('api/login/', CustomLoginView.as_view(), name='token_obtain_pair'),
    path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # ViewSet API endpoints
    path('api/', include(router.urls)),
    path('api/customer_profile/', customer_profile, name='customer_profile'),
    path('api/change-password/', ChangePasswordView.as_view(), name='change-password'),

    # HTML pages
    path('', views.home, name='home'), 
    path('checkout/', views.checkout, name='checkout'),
    path('comfirmation/', views.confirmation, name='confirmation'),
    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
    path('login/', views.login, name='login'),
    path('productDetail/', views.productDetail, name='productDetail'),
    path('shop/', views.shop, name='shop'),
    path('register/', views.register, name='register'),
    path('shoppingCart/', views.shoppingCart, name='shoppingCart'),
    path('contact/', views.contact, name='contact'),
    path('account/', views.account, name='account'),

    path('blog/', views.blog, name= 'blog'),
    path('blog/<int:id>/', views.blog_details, name='blogDetails'),
    path('blog/<int:id>/', views.blogbreadcrumb_details, name='blogDetails'),

    path('featuredProducts/', views.featuredProducts, name='featuredProducts'),
    path('shop/<int:id>/', views.productbreadcrumb_details, name='productDetails'),
    path('shop/<int:id>/', views.product_details, name='productDetails'),
]

