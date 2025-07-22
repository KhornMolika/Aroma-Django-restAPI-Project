from django.contrib.auth.models import User
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

class ImageType(models.Model): 
    imageTypeName = models.CharField(max_length=200, null=True) 
    def __str__(self):          
        return f'{self.id} | {self.imageTypeName}'
    
class Image(models.Model): 
    imageName = models.CharField(max_length=200, null=True) 
    imageURL = models.ImageField(upload_to='images/Dynamic/',null=True,blank=True) 
    imageLink = models.CharField(max_length=200, null=True) 
    imageTypeID = models.ForeignKey(ImageType, on_delete=models.CASCADE, null=True) 
    active = models.CharField(max_length=200, null=True) 
    imageDate = models.DateTimeField(auto_now_add=True, null=True) 
    def __str__(self):          
        return f'{self.id} | {self.imageName}'


class Category(models.Model):
    categoryName = models.CharField(max_length=200, null=True)
    def __str__(self):         
        return f'{self.id} | {self.categoryName}'
    
class Product(models.Model):
    productName = models.CharField(max_length=200, null=True)
    categoryID = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    unitPrice = models.DecimalField(max_digits=10, decimal_places=2)
    productDescript =  RichTextUploadingField(null=True)
    productImage = models.ImageField(upload_to='images/Products/',null=True,blank=True)
    productDate = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):         
        return f'{self.id} | {self.productName}'

class ProductDetail(models.Model):
    productID = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    availability = models.CharField(max_length=200, null=True)
    stock = models.PositiveIntegerField(default=0)
    brand = models.CharField(max_length=200, null=True)
    size = models.CharField(max_length=200, null=True)
    condition = models.CharField(max_length=200, null=True)
    material = models.CharField(max_length=200, null=True)
    color = models.CharField(max_length=200, null=True)
    productDetailDate = models.DateTimeField (auto_now_add=True, null=True)
    def __str__(self):         
        return f'{self.productID} - {self.productID.productName}'

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10, blank=True)
    profileImage = models.ImageField(upload_to='images/profile/',null=True,blank=True)

    def __str__(self):
        return f'cusID : {self.id} - {self.user.username}'

class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return sum(item.subtotal() for item in self.cartitem_set.all())

    def __str__(self):
        return f"Cart : {self.id} for {self.customer.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
        
       
class QRCode(models.Model):
    qrName = models.CharField(max_length=100)
    qrImage = models.ImageField(upload_to='images/qrcodes/')

    def __str__(self):
        return self.qrName


class Address(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='addresses')
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    address_type = models.CharField(
        max_length=50,
        choices=[('home', 'Home'), ('work', 'Work'), ('other', 'Other')],
        default='home'
    )
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Address : {self.id} - {self.street}, {self.city}"


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    shipping_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    order_date = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    qr_invoice = models.ImageField(upload_to='images/QRCodeInvoice/', null=True, blank=True)
    payment_proof = models.ImageField(upload_to='images/PaymentProof/', null=True, blank=True)

    def total_amount(self):
        return sum(item.subtotal for item in self.orderitem_set.all())

    def __str__(self):
        return f"Order : {self.id} by {self.customer.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)  # current price from Product
    store_price = models.DecimalField(max_digits=10, decimal_places=2)    # stored price at purchase time
    quantity = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.store_price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order #{self.order.id}"

class BlogCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"BlogCatID : {self.id} - {self.name}"

class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='blogs/')
    author = models.CharField(max_length=100)
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, related_name='blogs')
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class BlogDetail(models.Model):
    blog = models.OneToOneField(Blog, on_delete=models.CASCADE, related_name='details')
    subtitle = models.CharField(max_length=255)
    body = models.TextField()

    def __str__(self):
        return f"Details of {self.blog.title}"

class BlogComment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=150, blank=True)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.name} on {self.blog.title}"

class Feedback(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    message = models.TextField()
    rating = models.PositiveIntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.rating} stars for {self.product.name}"


