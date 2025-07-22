from rest_framework.routers import DefaultRouter
from .views import *
from . import views
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()

router.register(r'users', UserViewSet, basename='user')
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'addresses', AddressViewSet, basename='addresses')

router.register(r'image-types', ImageTypeViewSet, basename='imagetype')
router.register(r'images', ImageViewSet, basename='image')

router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'product-details', ProductDetailViewSet, basename='productdetail')
router.register(r'feedbacks', FeedbackViewSet, basename='feedback')

router.register(r'cart-items', CartItemViewSet, basename='cartitem')
router.register(r'carts', CartViewSet, basename='cart')

router.register(r'qrcodes', QRCodeViewSet, basename='qrcode')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'order-items', OrderItemViewSet, basename='orderitem')

router.register(r'blog-categories', BlogCategoryViewSet, basename='blogcategory')
router.register(r'blogs', BlogViewSet, basename='blog')
router.register(r'blog-details', BlogDetailViewSet, basename='blogdetail')
router.register(r'blog-comments', BlogCommentViewSet, basename='blogcomment')


urlpatterns = [
    path('api/register/', RegisterAPIView.as_view(), name='register'),

    path('api/login/', CustomLoginView.as_view(), name='token_obtain_pair'),
    path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/', include(router.urls)),
    path('blog/', views.blog, name= 'blog'),
    path('blogDetails/', views.blogDetails, name= 'blogDetails'),
    path('checkout/', views.checkout, name= 'checkout'),
    path('comfirmation/', views.confirmation, name= 'confirmation'),
    path('forgotPassword/', views.forgotPassword, name= 'forgotPassword'),
    path('', views.home, name= 'home'),
    path('login/', views.login, name= 'login'),
    path('productDetail/', views.productDetail, name= 'productDetail'),
    path('shop/', views.shop, name= 'shop'),
    path('register/', views.register, name= 'register'),
    path('shoppingCart/', views.shoppingCart, name= 'shoppingCart'),
    path('contact/', views.contact, name= 'contact'),
    path('account/', views.account, name= 'account'),
    path('editProfile/', views.editProfile, name= 'editProfile'),

]

