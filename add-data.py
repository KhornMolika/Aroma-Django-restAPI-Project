
import os
import django
from decimal import Decimal
from django.utils import timezone
import requests
from django.core.files.base import ContentFile
from urllib.parse import urlparse
import sys

# Setup Django environment - change 'aroma_api' to your project name if different
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aroma_api.settings')
django.setup()

from core.models import Product, ProductDetail, Category

import os
import django
from decimal import Decimal
from django.utils import timezone
import requests
from django.core.files.base import ContentFile
from urllib.parse import urlparse

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aroma_api.settings')
django.setup()

from core.models import Product, ProductDetail, Category, BlogCategory, Blog, BlogDetail

# Category mapping
category_map = {
    "Women's Clothing": 1,
    "Men's Clothing": 2,
    "Shoes": 3,
    "Accessories": 4,
    "Bags": 5,
}

products_by_category = {
    "Women's Clothing": [
        {
            "name": "Adidas Originals Denim Track Jacket",
            "price": "90.00",
            "description": "Stylish denim track jacket from Adidas Originals with 3-Stripes and Trefoil logo.",
            "image_link": "http://googleusercontent.com/file_content/0",
            "stock": 180,
            "brand": "Adidas",
            "size": "XS, S, M, L, XL",
            "condition": "New",
            "material": "Denim",
            "color": "Mid-wash Blue"
        },
        {
            "name": "Loose Fit Striped T-Shirt Dress",
            "price": "55.00",
            "description": "Navy and white striped oversized t-shirt dress with relaxed fit.",
            "image_link": "http://googleusercontent.com/file_content/1",
            "stock": 200,
            "brand": "Generic",
            "size": "XS, S, M, L, XL",
            "condition": "New",
            "material": "Cotton",
            "color": "Navy/White"
        },
        {
            "name": "Leopard Print Overshirt Jacket",
            "price": "75.00",
            "description": "Bold leopard print overshirt jacket perfect for layering.",
            "image_link": "http://googleusercontent.com/file_content/2",
            "stock": 120,
            "brand": "Generic",
            "size": "XS, S, M, L",
            "condition": "New",
            "material": "Polyester",
            "color": "Leopard Print"
        },
        {
            "name": "Layered Trench Coat with Hooded Insert",
            "price": "180.00",
            "description": "Modern trench coat with detachable hooded insert, burgundy color.",
            "image_link": "http://googleusercontent.com/file_content/3",
            "stock": 90,
            "brand": "Generic",
            "size": "XS, S, M, L",
            "condition": "New",
            "material": "Cotton Blend",
            "color": "Burgundy"
        },
        {
            "name": "Classic Beige Trench Coat with Plaid Details",
            "price": "170.00",
            "description": "Double-breasted beige trench coat with plaid lining.",
            "image_link": "http://googleusercontent.com/file_content/4",
            "stock": 100,
            "brand": "Generic",
            "size": "XS, S, M, L",
            "condition": "New",
            "material": "Polyester",
            "color": "Beige"
        },
        {
            "name": "Flowing Taupe Trench Coat",
            "price": "160.00",
            "description": "Elegant taupe trench coat with relaxed silhouette.",
            "image_link": "http://googleusercontent.com/file_content/5",
            "stock": 110,
            "brand": "Generic",
            "size": "XS, S, M, L",
            "condition": "New",
            "material": "Polyester",
            "color": "Taupe"
        },
        {
            "name": "Cropped Beige Trench Jacket",
            "price": "110.00",
            "description": "Cropped trench jacket with oversized collar and buckle sleeves.",
            "image_link": "http://googleusercontent.com/file_content/6",
            "stock": 130,
            "brand": "Generic",
            "size": "XS, S, M, L",
            "condition": "New",
            "material": "Cotton Blend",
            "color": "Beige"
        },
        {
            "name": "Light Green Shirred Bandeau Top & Shorts Set",
            "price": "85.00",
            "description": "Two-piece set with shirred bandeau top and drawstring shorts.",
            "image_link": "http://googleusercontent.com/file_content/7",
            "stock": 150,
            "brand": "Generic",
            "size": "XS, S, M, L",
            "condition": "New",
            "material": "Linen",
            "color": "Light Green"
        },
        {
            "name": "White Halter Neck Tiered Midi Dress",
            "price": "120.00",
            "description": "White midi dress with halter neckline and tiered A-line skirt.",
            "image_link": "http://googleusercontent.com/file_content/8",
            "stock": 100,
            "brand": "Generic",
            "size": "XS, S, M, L",
            "condition": "New",
            "material": "Cotton",
            "color": "White"
        },
        {
            "name": "Oversized Lilac Striped Button-Up Shirt",
            "price": "60.00",
            "description": "Relaxed oversized button-up shirt with lilac stripes.",
            "image_link": "http://googleusercontent.com/file_content/9",
            "stock": 140,
            "brand": "Generic",
            "size": "XS, S, M, L, XL",
            "condition": "New",
            "material": "Cotton",
            "color": "Lilac/White"
        },
    ],

    "Men's Clothing":[
        {
            "name": "Essential Black Nylon Belt Bag",
            "price": "30.00",
            "description": "A versatile and practical black nylon belt bag (fanny pack) with a minimalist design. Features a main zippered compartment and adjustable strap, perfect for carrying essentials on the go.",
            "image_link": "http://127.0.0.1:8000/media/images/Products/205990883-2.jpg",
            "stock": 250,
            "brand": "Generic",
            "size": "Adjustable Strap",
            "condition": "New",
            "material": "Nylon",
            "color": "Black"
        },
        {
            "name": "Adidas Originals Denim Track Jacket",
            "price": "90.00",
            "description": "A stylish take on a classic, this Adidas Originals track jacket is crafted from mid-wash denim. Features the iconic 3-Stripes down the sleeves and Trefoil logo, blending sporty heritage with streetwear.",
            "image_link": "http://127.0.0.1:8000/media/images/Products/207980560-2.jpg",
            "stock": 180,
            "brand": "Adidas",
            "size": "XS, S, M, L, XL",
            "condition": "New",
            "material": "Denim",
            "color": "Mid-wash Blue"
        },
        {
            "name": "Classic Black Leather Shirt Jacket",
            "price": "180.00",
            "description": "A sophisticated shirt-style jacket made from premium black leather with a subtle pebbled texture. Features a classic collar, button-front closure, and chest pockets, offering a versatile layering piece.",
            "image_link": "http://127.0.0.1:8000/media/images/Products/61qVUUJ8YkL.jpg",
            "stock": 90,
            "brand": "Generic",
            "size": "S, M, L, XL",
            "condition": "New",
            "material": "Genuine Leather",
            "color": "Black"
        },
        {
            "name": "Brown Stand-Collar Faux Leather Jacket",
            "price": "120.00",
            "description": "A sleek brown faux leather jacket with a modern stand collar and multiple zip and flap pockets for a utilitarian edge. Offers a rugged yet refined look, ideal for everyday wear.",
            "image_link": "http://127.0.0.1:8000/media/images/Products/65a9738aa4a7283d7f7a7678-dtydtpe-leather-jacket-men-men-s-winter.jpg",
            "stock": 110,
            "brand": "Generic",
            "size": "S, M, L, XL",
            "condition": "New",
            "material": "Faux Leather",
            "color": "Brown"
        },
        {
            "name": "Charcoal Herringbone Wool Blend Suit Jacket",
            "price": "280.00",
            "description": "A sophisticated men's suit jacket crafted from a premium wool blend with a distinctive charcoal herringbone pattern. Features a notched lapel and tailored fit, suitable for formal or elevated casual looks.",
            "image_link": "http://127.0.0.1:8000/media/images/Products/1920x2560.jpg",
            "stock": 70,
            "brand": "Generic",
            "size": "S, M, L, XL",
            "condition": "New",
            "material": "Wool Blend",
            "color": "Charcoal"
        },
        {
            "name": "Adidas Originals Black Track Jacket",
            "price": "85.00",
            "description": "A classic Adidas Originals full-zip track jacket in black, featuring the iconic white 3-Stripes down the sleeves and Trefoil logo on the chest. Made from comfortable polyester, perfect for athletic or casual wear.",
            "image_link": "http://127.0.0.1:8000/media/images/Products/205271107-2.jpg",
            "stock": 200,
            "brand": "Adidas",
            "size": "XS, S, M, L, XL",
            "condition": "New",
            "material": "Polyester",
            "color": "Black"
        },
        {
            "name": "Olive Green Bomber Jacket",
            "price": "95.00",
            "description": "A classic bomber jacket in a versatile olive green, featuring ribbed cuffs and hem, and a utility pocket on the sleeve. Offers a relaxed fit and durable construction, ideal for layering.",
            "image_link": "http://127.0.0.1:8000/media/images/Products/80f5a72b7dd7ac4aaede7fb08400cd18.jpg",
            "stock": 150,
            "brand": "Generic",
            "size": "S, M, L, XL",
            "condition": "New",
            "material": "Polyester",
            "color": "Olive Green"
        },
        {
            "name": "Bright Yellow Utility Hooded Jacket",
            "price": "75.00",
            "description": "A vibrant yellow hooded utility jacket with multiple large flap pockets, combining practical design with a bold color statement. Features a full-zip front and adjustable hood.",
            "image_link": "http://127.0.0.1:8000/media/images/Products/61gdH5qf08L._UY1000_.jpg",
            "stock": 100,
            "brand": "Generic",
            "size": "S, M, L, XL",
            "condition": "New",
            "material": "Polyester",
            "color": "Bright Yellow"
        },
        {
            "name": "Adidas Originals 'Casual Sports Club' Graphic Tee",
            "price": "40.00",
            "description": "A black cotton t-shirt from Adidas Originals featuring a playful graphic print of a leopard wearing a baseball cap with 'CASUAL SPORTS CLUB' text. Offers a relaxed fit and crew neck.",
            "image_link": "http://127.0.0.1:8000/media/images/Products/208736827-2.jpg",
            "stock": 190,
            "brand": "Adidas",
            "size": "S, M, L, XL",
            "condition": "New",
            "material": "Cotton",
            "color": "Black"
        },
        {
            "name": "Cream 'Thailand' Embroidered T-Shirt",
            "price": "35.00",
            "description": "A cream-colored cotton t-shirt with subtle 'THAILAND' embroidery on the chest, offering a relaxed fit and classic crew neck. Perfect for a casual, travel-inspired look.",
            "image_link": "http://127.0.0.1:8000/media/images/Products/208320490-2.jpg",
            "stock": 220,
            "brand": "Generic",
            "size": "S, M, L, XL",
            "condition": "New",
            "material": "Cotton",
            "color": "Cream"
        }
    ],

    "Shoes": [
        {
            "name": "Adidas Gazelle Blackout Suede Sneakers",
            "price": "90.00",
            "description": "Black suede Gazelle sneakers from Adidas.",
            "image_link": "http://googleusercontent.com/file_content/0",
            "stock": 200,
            "brand": "Adidas",
            "size": "US Men's 6-13, US Women's 5-12",
            "condition": "New",
            "material": "Suede",
            "color": "Black"
        },
        {
            "name": "Dr. Martens Quad Sole Combat Boots",
            "price": "190.00",
            "description": "Chunky combat boots with Quad sole from Dr. Martens.",
            "image_link": "http://googleusercontent.com/file_content/1",
            "stock": 150,
            "brand": "Dr. Martens",
            "size": "US Unisex 5-12",
            "condition": "New",
            "material": "Leather",
            "color": "Black"
        },
        {
            "name": "Raffia Buckle Platform Sandals",
            "price": "85.00",
            "description": "Stylish platform sandals with natural raffia upper.",
            "image_link": "http://googleusercontent.com/file_content/2",
            "stock": 130,
            "brand": "Generic",
            "size": "US Women's 5-10",
            "condition": "New",
            "material": "Raffia",
            "color": "Natural"
        },
        {
            "name": "Dr. Martens Tassel Loafers - Oxblood",
            "price": "150.00",
            "description": "Classic loafers in oxblood polished leather with tassels.",
            "image_link": "http://googleusercontent.com/file_content/3",
            "stock": 100,
            "brand": "Dr. Martens",
            "size": "US Unisex 6-12",
            "condition": "New",
            "material": "Leather",
            "color": "Oxblood"
        },
        {
            "name": "Adidas Samba Burgundy & White Sneakers",
            "price": "100.00",
            "description": "Adidas Samba sneakers in burgundy and white.",
            "image_link": "http://googleusercontent.com/file_content/4",
            "stock": 180,
            "brand": "Adidas",
            "size": "US Men's 6-13, US Women's 5-12",
            "condition": "New",
            "material": "Suede",
            "color": "Burgundy/White"
        },
        {
            "name": "Chunky Black Loafers",
            "price": "110.00",
            "description": "Modern chunky black loafers.",
            "image_link": "http://googleusercontent.com/file_content/5",
            "stock": 160,
            "brand": "Generic",
            "size": "US Unisex 6-12",
            "condition": "New",
            "material": "Leather",
            "color": "Black"
        },
        {
            "name": "ASICS GEL-NYC Grey & Yellow Sneakers",
            "price": "140.00",
            "description": "ASICS sneakers blending classic GEL models with modern design.",
            "image_link": "http://googleusercontent.com/file_content/6",
            "stock": 140,
            "brand": "ASICS",
            "size": "US Unisex 6-12",
            "condition": "New",
            "material": "Mesh/Synthetic",
            "color": "Grey/Yellow"
        },
        {
            "name": "Black Pointed Slingback Kitten Heels",
            "price": "80.00",
            "description": "Elegant black slingback kitten heels.",
            "image_link": "http://googleusercontent.com/file_content/7",
            "stock": 120,
            "brand": "Generic",
            "size": "US Women's 5-10",
            "condition": "New",
            "material": "Leather",
            "color": "Black"
        },
        {
            "name": "Adidas Spezial Brown Suede Gum Sole Sneakers",
            "price": "95.00",
            "description": "Brown suede Spezial sneakers with gum sole.",
            "image_link": "http://googleusercontent.com/file_content/8",
            "stock": 170,
            "brand": "Adidas",
            "size": "US Men's 6-13, US Women's 5-12",
            "condition": "New",
            "material": "Suede",
            "color": "Brown"
        },
        {
            "name": "Adidas Samba Cream & Brown Sneakers",
            "price": "100.00",
            "description": "Cream leather Samba sneakers with brown stripes.",
            "image_link": "http://googleusercontent.com/file_content/9",
            "stock": 180,
            "brand": "Adidas",
            "size": "US Men's 6-13, US Women's 5-12",
            "condition": "New",
            "material": "Leather/Suede",
            "color": "Cream/Brown"
        },
    ],

    "Accessories": [
        {
            "name": "Gold Leaf Pendant Necklace",
            "price": "30.00",
            "description": "Delicate gold-tone necklace featuring leaf-shaped pendants.",
            "image_link": "http://googleusercontent.com/file_content/0",
            "stock": 250,
            "brand": "Generic",
            "size": "One Size",
            "condition": "New",
            "material": "Gold-Plated Alloy",
            "color": "Gold"
        },
        {
            "name": "Pearl and Shell Drop Earrings",
            "price": "70.00",
            "description": "Elegant drop earrings combining pearls and shell details.",
            "image_link": "http://googleusercontent.com/file_content/1",
            "stock": 90,
            "brand": "Generic",
            "size": "One Size",
            "condition": "New",
            "material": "Pearls / Shell",
            "color": "White/Gold"
        },
        {
            "name": "Wide Floral Cuff Bracelet",
            "price": "60.00",
            "description": "Bold gold-tone cuff bracelet with intricate floral cutouts.",
            "image_link": "http://googleusercontent.com/file_content/2",
            "stock": 80,
            "brand": "Generic",
            "size": "Adjustable",
            "condition": "New",
            "material": "Gold-Plated Metal",
            "color": "Gold"
        },
        {
            "name": "Greek Key Pattern Band Ring",
            "price": "25.00",
            "description": "Silver-tone band ring engraved with Greek key pattern.",
            "image_link": "http://googleusercontent.com/file_content/3",
            "stock": 180,
            "brand": "Generic",
            "size": "6, 7, 8, 9",
            "condition": "New",
            "material": "Stainless Steel",
            "color": "Silver"
        },
        {
            "name": "Abstract Star Statement Ring",
            "price": "35.00",
            "description": "Unique silver-tone ring in abstract star shape design.",
            "image_link": "http://googleusercontent.com/file_content/4",
            "stock": 140,
            "brand": "Generic",
            "size": "6, 7, 8",
            "condition": "New",
            "material": "Alloy",
            "color": "Silver"
        },
        {
            "name": "Red Gemstone Rectangular Ring",
            "price": "40.00",
            "description": "Gold-tone rectangular ring with striking red gemstone centerpiece.",
            "image_link": "http://googleusercontent.com/file_content/5",
            "stock": 120,
            "brand": "Generic",
            "size": "6, 7, 8",
            "condition": "New",
            "material": "Gold-Plated Alloy / Gemstone",
            "color": "Gold/Red"
        },
        {
            "name": "Gold Flower Stud Earrings",
            "price": "20.00",
            "description": "Small gold-tone earrings shaped as delicate flowers.",
            "image_link": "http://googleusercontent.com/file_content/6",
            "stock": 160,
            "brand": "Generic",
            "size": "One Size",
            "condition": "New",
            "material": "Gold-Plated Alloy",
            "color": "Gold"
        },
        {
            "name": "Triple Floral Drop Earrings",
            "price": "50.00",
            "description": "Charming gold-tone drop earrings featuring three floral motifs.",
            "image_link": "http://googleusercontent.com/file_content/7",
            "stock": 90,
            "brand": "Generic",
            "size": "One Size",
            "condition": "New",
            "material": "Gold-Plated Alloy",
            "color": "Gold"
        },
        {
            "name": "Minimalist Silver Band Ring",
            "price": "15.00",
            "description": "Sleek and simple silver-tone minimalist band ring.",
            "image_link": "http://googleusercontent.com/file_content/8",
            "stock": 200,
            "brand": "Generic",
            "size": "6, 7, 8, 9",
            "condition": "New",
            "material": "Stainless Steel",
            "color": "Silver"
        }
    ],

    "Bags": [
        {
            "name": "Adidas Large 3-Stripes Essential Backpack",
            "price": "55.00",
            "description": "Spacious Adidas backpack with 3-Stripes and Badge of Sport.",
            "image_link": "http://googleusercontent.com/file_content/0",
            "stock": 200,
            "brand": "Adidas",
            "size": "One Size",
            "condition": "New",
            "material": "Polyester",
            "color": "Black"
        },
        {
            "name": "Large Olive Green Backpack",
            "price": "65.00",
            "description": "Classic olive green backpack with zippered compartments.",
            "image_link": "http://googleusercontent.com/file_content/1",
            "stock": 150,
            "brand": "Generic",
            "size": "One Size",
            "condition": "New",
            "material": "Polyester",
            "color": "Olive Green"
        },
        {
            "name": "TOPSHOP Brown Embossed Logo Tote Bag",
            "price": "40.00",
            "description": "Casual brown tote bag with TOPSHOP logo embossing.",
            "image_link": "http://googleusercontent.com/file_content/2",
            "stock": 120,
            "brand": "TOPSHOP",
            "size": "One Size",
            "condition": "New",
            "material": "Synthetic",
            "color": "Brown"
        },
        {
            "name": "TOPSHOP Black Woven Detail Tote Bag",
            "price": "70.00",
            "description": "Stylish tote with woven detail and stud accents.",
            "image_link": "http://googleusercontent.com/file_content/3",
            "stock": 90,
            "brand": "TOPSHOP",
            "size": "One Size",
            "condition": "New",
            "material": "Synthetic",
            "color": "Black"
        },
        {
            "name": "Metallic Silver Ring Handle Clutch Bag",
            "price": "60.00",
            "description": "Chic silver clutch with metal ring handle.",
            "image_link": "http://googleusercontent.com/file_content/4",
            "stock": 80,
            "brand": "Generic",
            "size": "One Size",
            "condition": "New",
            "material": "Metallic Synthetic",
            "color": "Silver"
        },
        {
            "name": "Light Blue Cotton Canvas Tote Bag",
            "price": "25.00",
            "description": "Versatile cotton canvas tote for daily use.",
            "image_link": "http://googleusercontent.com/file_content/5",
            "stock": 180,
            "brand": "Generic",
            "size": "One Size",
            "condition": "New",
            "material": "Cotton",
            "color": "Light Blue"
        },
        {
            "name": "Carhartt WIP Small Black Crossbody Bag",
            "price": "45.00",
            "description": "Small crossbody bag with durable design.",
            "image_link": "http://googleusercontent.com/file_content/6",
            "stock": 160,
            "brand": "Carhartt WIP",
            "size": "One Size",
            "condition": "New",
            "material": "Polyester",
            "color": "Black"
        },
        {
            "name": "Burgundy Woven Panel Tote Bag",
            "price": "80.00",
            "description": "Burgundy tote with stylish woven panel design.",
            "image_link": "http://googleusercontent.com/file_content/7",
            "stock": 70,
            "brand": "Generic",
            "size": "One Size",
            "condition": "New",
            "material": "Synthetic",
            "color": "Burgundy"
        },
        {
            "name": "Soft Black Multi-Pocket Hobo Bag",
            "price": "75.00",
            "description": "Slouchy hobo bag with multiple pockets.",
            "image_link": "http://googleusercontent.com/file_content/8",
            "stock": 100,
            "brand": "Generic",
            "size": "One Size",
            "condition": "New",
            "material": "Synthetic",
            "color": "Black"
        },
        {
            "name": "Levi's Olive Green Classic Backpack",
            "price": "50.00",
            "description": "Durable Levi's backpack in olive green shade.",
            "image_link": "http://googleusercontent.com/file_content/9",
            "stock": 170,
            "brand": "Levi's",
            "size": "One Size",
            "condition": "New",
            "material": "Polyester",
            "color": "Olive Green"
        },
    ]
}

def insert_products(products_by_category):
    for category_name, products in products_by_category.items():
        try:
            category = Category.objects.get(id=category_map[category_name])
        except Category.DoesNotExist:
            print(f"Category '{category_name}' does not exist.")
            continue

        for item in products:
            product = Product(
                productName=item['name'],
                categoryID=category,
                unitPrice=Decimal(item['price']),
                productDescript=item['description'],
                productDate=timezone.now()
            )

            # Download and attach image
            try:
                response = requests.get(item['image_link'])
                response.raise_for_status()
                img_name = os.path.basename(urlparse(item['image_link']).path)
                if not img_name:
                    img_name = f"{item['name'].replace(' ', '_')}.jpg"
                product.productImage.save(img_name, ContentFile(response.content), save=False)
            except Exception as e:
                print(f"Failed to download image for '{item['name']}': {e}")

            product.save()

            # Create ProductDetail
            ProductDetail.objects.create(
                productID=product,
                availability="In Stock",
                stock=item['stock'],
                brand=item.get('brand', 'Generic'),
                size=item.get('size', 'Free Size'),
                condition=item.get('condition', 'New'),
                material=item.get('material', 'Unknown'),
                color=item.get('color', 'Various')
            )

            print(f"Added {item['name']} to {category_name}")

# insert_products(products_by_category)


# Full JSON for 20 Blog and BlogDetail entries
blogs_data = [
    {
        "blog": {
            "title": "Embracing a Greener Future",
            "content": "Discover how small lifestyle changes can contribute to a more sustainable world. Learn practical tips for reducing waste, saving energy, and making environmentally conscious choices.",
            "image": "blogs/green_future.jpg",
            "author": "Alice",
            "category_name": "Sustainability",
            "subtitle": "Embracing a Greener Future",
            "body": "Sustainability starts at home. Whether it's turning off lights when leaving a room or bringing your own bags to the store, every action adds up. A green future depends on the mindful habits we form today. Small choices like reducing water waste, eating seasonal and locally sourced foods, or composting kitchen scraps help lower your ecological footprint. By conserving energy and reducing plastic use, you contribute to cleaner air and water for everyone. It's important to educate family and friends to build a community-wide commitment to the environment. Sustainability isn't about perfection but progress—each step forward brings us closer to preserving our planet. Remember, innovation and technology also play roles, with renewable energy sources and eco-friendly products becoming more accessible. Ultimately, living sustainably is about respecting nature and ensuring future generations enjoy the same beauty and resources we do today. Embracing a greener future means living consciously every day."
        }
    },
    {
        "blog": {
            "title": "Small Steps, Big Impact",
            "content": "You don't have to change everything overnight. Learn how simple habits like recycling and reusing can lead to long-term environmental benefits.",
            "image": "blogs/small_steps.jpg",
            "author": "Bob",
            "category_name": "Sustainability",
            "subtitle": "Small Actions, Lasting Change",
            "body": "It's easy to underestimate the power of small daily changes. Choosing to bike instead of drive or refusing single-use plastics may seem minor—but over time, these decisions add up to significant global impact. Recycling not only reduces landfill but conserves raw materials and energy needed to produce new products. Reusing items extends their lifecycle, preventing waste and pollution. Every plastic bottle recycled is one less in the ocean. Conserving electricity by unplugging unused devices lowers greenhouse gas emissions linked to power generation. Planting trees or supporting reforestation projects helps restore habitats and absorb carbon dioxide. Simple habits like carrying a reusable water bottle or coffee cup may seem trivial but foster a mindset of responsibility. The ripple effect is strong—encouraging others to adopt these habits creates collective momentum. These small steps, when combined, contribute to a healthier planet, proving individual choices truly matter."
        }
    },
    {
        "blog": {
            "title": "Eco-Friendly Fashion",
            "content": "Learn how your wardrobe choices affect the planet. Discover ethical brands, sustainable materials, and how to dress responsibly.",
            "image": "blogs/eco_fashion.jpg",
            "author": "Diana",
            "category_name": "Sustainability",
            "subtitle": "Fashion That Cares",
            "body": "Sustainable fashion focuses on quality over quantity, using materials like organic cotton and recycled fibers. Supporting ethical brands and shopping secondhand helps reduce waste in the fashion industry. Fast fashion produces enormous textile waste and pollution, but choosing eco-friendly fabrics lowers the environmental footprint. Materials like hemp, bamboo, and Tencel require less water and pesticides during production. Many designers now prioritize fair labor practices, ensuring garment workers are paid fairly and work in safe conditions. When you buy fewer, better-quality pieces, clothes last longer and reduce the demand for new resources. Thrifting and swapping clothes with friends promote reuse and style diversity. Repairing or altering garments instead of discarding them prevents textiles from piling in landfills. Eco-friendly fashion also embraces timeless styles rather than fleeting trends. By consciously curating your wardrobe, you can make a positive impact on the planet and support a more just and sustainable industry."
        }
    },
    {
        "blog": {
            "title": "The Power of Reuse",
            "content": "Reusing and repurposing old items can reduce your footprint and boost creativity. Explore fun and useful ways to give new life to everyday objects.",
            "image": "blogs/power_of_reuse.jpg",
            "author": "Edward",
            "category_name": "Sustainability",
            "subtitle": "Repurpose and Reinvent",
            "body": "Instead of tossing out jars, boxes, or clothing, think of new uses for them. Upcycling encourages creativity and keeps items out of landfills, helping create a circular economy. Glass jars can be repurposed as storage containers, candle holders, or planters. Old clothes can become cleaning rags, patchwork quilts, or bags. Cardboard boxes serve as organizers or crafting materials for kids. Reusing materials saves money and reduces demand for new manufacturing, which often consumes large amounts of energy and water. Repurposed items add charm and personality to your home, making your space uniquely yours. Workshops and online communities share ideas and tutorials, fostering a culture of resourcefulness. When reuse becomes habit, less waste is produced, and environmental impact decreases. Celebrating the power of reuse means valuing materials for their full lifecycle, transforming “trash” into treasures with imagination and care."
        }
    },
    {
        "blog": {
            "title": "Community and Climate",
            "content": "Local efforts can have a global impact. Discover how community-based sustainability projects are changing the world one neighborhood at a time.",
            "image": "blogs/community_climate.jpg",
            "author": "Charlie",
            "category_name": "Sustainability",
            "subtitle": "Together for the Planet",
            "body": "From community gardens to local clean-up drives, small groups are making a big difference. Collaboration fosters accountability and spreads environmental awareness at a grassroots level. Community projects provide education and hands-on opportunities to engage in sustainable living. Urban gardens increase green spaces, improve air quality, and supply fresh produce to neighborhoods. Clean-up events remove litter from parks and waterways, protecting wildlife and improving public health. Group efforts can also influence local policies by showing demand for sustainable practices. Sharing resources like tools or compost bins reduces consumption and waste. Events that celebrate Earth Day or sustainability milestones build connections and inspire others. Local businesses that embrace eco-friendly practices contribute to greener economies. Ultimately, when individuals unite, their combined actions create a powerful force for environmental change. Together, communities can build resilience and pave the way for a healthier planet."
        }
    },
    {
        "blog": {
            "title": "Dressing for Your Body Type",
            "content": "Style isn't one-size-fits-all. Find tips on how to dress according to your body shape and highlight your best features.",
            "image": "blogs/body_type.jpg",
            "author": "Bella",
            "category_name": "Fashion Tips",
            "subtitle": "Style that Suits You",
            "body": "Understanding your shape—pear, apple, rectangle, or hourglass—helps you select cuts and patterns that flatter your figure. For pear shapes, balance hips with attention-grabbing tops, like bright colors or interesting necklines. Apple shapes benefit from structured jackets and empire waists that define the midsection. Rectangles can create curves with belts and layered pieces. Hourglass figures shine in tailored clothing that highlights the waist. Fabrics and prints also play roles; vertical stripes elongate, while bold patterns emphasize areas. Comfortable shoes and properly fitted undergarments enhance overall confidence. Dressing for your body type is not about hiding flaws but celebrating your unique silhouette. When you wear what complements your shape, your posture improves and you naturally exude style and grace. Learning these tips empowers you to build a wardrobe that feels authentic and boosts self-esteem."
        }
    },
    {
        "blog": {
            "title": "Wardrobe Essentials",
            "content": "Build a strong foundation for your wardrobe with these timeless, versatile essentials every person should own.",
            "image": "blogs/wardrobe_essentials.jpg",
            "author": "Alice",
            "category_name": "Fashion Tips",
            "subtitle": "Classic Pieces That Never Go Out of Style",
            "body": "Think white shirts, black jeans, denim jackets, and clean sneakers. These items serve as a base for endless outfit combinations and are worth investing in. A well-fitted blazer can instantly elevate casual looks for work or events. Neutral-colored sweaters and cardigans offer layering options across seasons. Classic accessories like leather belts and simple watches add polish without overpowering. Versatile dresses in solid colors or subtle patterns transition from day to night with the right shoes and jewelry. Quality materials last longer, making them more sustainable and cost-effective over time. Organizing your essentials keeps your closet functional and inspires creativity. When you own timeless staples, you can mix and match with trendier pieces without clutter. These wardrobe foundations ensure you're always prepared for any occasion with style and ease."
        }
    },
    {
        "blog": {
            "title": "Accessorize Wisely",
            "content": "The right accessories can elevate your entire look. Learn how to choose pieces that complement your outfit.",
            "image": "blogs/accessorize.jpg",
            "author": "Diana",
            "category_name": "Fashion Tips",
            "subtitle": "Small Details, Big Style",
            "body": "A statement necklace or a well-chosen scarf can transform even the simplest outfit. Accessories allow you to show personality while staying stylish. Choosing the right colors complements your clothing and skin tone, while textures add dimension. Mixing metals or layering delicate jewelry creates interest without overwhelming. Hats, belts, and bags serve both function and fashion, pulling looks together cohesively. For formal occasions, classic pearls or diamond studs never go out of style. Casual outfits come alive with colorful bracelets or patterned socks. Remember to balance—if your outfit is bold, opt for subtle accessories, and vice versa. Accessories also allow experimentation without major wardrobe changes. Investing in versatile pieces increases your options and refreshes your style with ease. Ultimately, accessorizing wisely enhances confidence and completes your look."
        }
    },
    {
        "blog": {
            "title": "Mix and Match Mastery",
            "content": "Discover the art of combining patterns, textures, and colors to create dynamic outfits from basic pieces.",
            "image": "blogs/mix_match.jpg",
            "author": "Charlie",
            "category_name": "Fashion Tips",
            "subtitle": "Unlocking Style Variety",
            "body": "Don't be afraid to mix prints or layer different fabrics. Mixing adds visual interest and maximizes your wardrobe's versatility. Pairing stripes with florals or plaids with polka dots can look modern when balanced by color palettes. Textures like leather, knitwear, and silk bring depth to outfits. Start simple by combining patterns of different scales or keeping colors in the same family. Layering garments lets you adapt to changing temperatures and adds dimension. Experiment with statement pieces, such as a bold jacket over basic tees. Accessories can unify mixed elements through matching colors or themes. Mastering mix and match reduces the need to buy more, as your existing clothes work harder for you. It encourages creativity and personal expression, helping your style evolve dynamically. With practice, mixing and matching becomes second nature and keeps your looks fresh."
        }
    },
    {
        "blog": {
            "title": "Seasonal Transitions",
            "content": "Learn how to keep your style fresh as the seasons change, using layering and smart styling techniques.",
            "image": "blogs/seasonal_transitions.jpg",
            "author": "Bob",
            "category_name": "Fashion Tips",
            "subtitle": "Fashion That Flows Through the Year",
            "body": "As the weather shifts, so can your outfits. Light jackets, cardigans, and scarves help bridge the gap between seasons while maintaining comfort and flair. Layering is key—start with breathable base layers and add insulating pieces that can be removed indoors. Transitioning prints and colors reflect seasonal moods; pastels and florals in spring, earth tones and plaids in autumn. Footwear shifts from sandals to ankle boots or loafers. Fabric choice matters too: cotton and linen for warmth, wool and cashmere for cooler days. Accessories like hats and gloves add warmth without bulk. Planning your wardrobe around versatile pieces ensures you don't overbuy for short periods. Paying attention to comfort and style during transitions helps you stay fashionable year-round. By mastering seasonal changes, you enjoy every month's unique palette and atmosphere."
        }
    },
    {
        "blog": {
            "title": "The Art of Upcycling",
            "content": "Upcycling turns waste into beauty. Find inspiration and techniques for creating something new from the old.",
            "image": "blogs/upcycling_art.jpg",
            "author": "Alice",
            "category_name": "Upcycling",
            "subtitle": "Creating with Purpose",
            "body": "Upcycling isn't just trendy—it's necessary. By reusing materials, we reduce landfill waste and foster a culture of creativity and sustainability. Upcycling transforms discarded items into functional or decorative pieces, often with a personal touch. This process saves energy compared to recycling, which can be resource-intensive. Common projects include turning pallets into furniture or old fabric into quilts. Upcycling also challenges consumerism by valuing what already exists. It promotes mindfulness about consumption and waste. Artists and crafters use upcycling to make unique, one-of-a-kind pieces that tell stories. Workshops and social media have popularized techniques, spreading ideas worldwide. This creative reuse empowers individuals to make environmental and economic impacts locally. Through upcycling, we turn trash into treasure, inspiring a shift toward a more circular economy and sustainable lifestyle."
        }
    },
    {
        "blog": {
            "title": "DIY with Denim",
            "content": "Got old jeans? Don't toss them—upcycle them! Discover easy and stylish projects to give denim a second life.",
            "image": "blogs/denim_diy.jpg",
            "author": "Edward",
            "category_name": "Upcycling",
            "subtitle": "Old Jeans, New Style",
            "body": "Denim is durable and versatile. With a few cuts and stitches, it can become bags, coasters, or even planters. Old jeans often accumulate holes or fade but hold potential for creative projects. Cut legs can turn into shorts, while pockets become handy storage pouches. Denim patches add character to worn clothes or repair tears stylishly. You can braid strips into rugs or weave them into baskets. Sewing a denim tote bag provides a reusable alternative to plastic carriers. Painting or embellishing denim adds a personal flair to garments or accessories. The thick fabric withstands wear, making it ideal for long-lasting projects. Repurposing denim saves waste from landfills and celebrates the material's rugged charm. With a little imagination and basic sewing skills, you can create practical and fashionable items that honor sustainability and creativity."
        }
    },
    {
        "blog": {
            "title": "Furniture Flip",
            "content": "You don't need to buy new to have beautiful furniture. Learn how to refresh old pieces with upcycling techniques.",
            "image": "blogs/furniture_flip.jpg",
            "author": "Bella",
            "category_name": "Upcycling",
            "subtitle": "Makeover on a Budget",
            "body": "A fresh coat of paint, new knobs, or fabric reupholstery can revive a tired piece. Upcycled furniture tells a story and saves money. Instead of buying new, give old chairs, tables, or dressers a second chance with sanding and refinishing. Chalk paint is popular for its ease and matte finish. Replacing hardware updates style instantly and adds personality. Recovering seats with colorful or textured fabric refreshes comfort and appearance. Repurposed furniture reduces demand for new resources like wood and metal. DIY tutorials and workshops provide step-by-step guidance, even for beginners. Customized furniture fits your space and taste uniquely. The process is rewarding, blending creativity and practicality. Upcycled pieces often become focal points in rooms, sparking conversations and admiration. Furniture flipping promotes sustainability, affordability, and personal expression all in one."
        }
    },
    {
        "blog": {
            "title": "Creative Gift Ideas",
            "content": "Upcycled gifts are heartfelt and eco-friendly. Discover DIY ideas that make great personalized presents.",
            "image": "blogs/gift_ideas.jpg",
            "author": "Diana",
            "category_name": "Upcycling",
            "subtitle": "Thoughtful, Sustainable Gifting",
            "body": "Handmade notebooks from old paper, photo frames from scrap wood, and sewn fabric totes are memorable gifts that show love and care for the planet. Upcycled gifts reflect thoughtfulness by turning waste into meaningful items. Personalized gifts often hold greater sentimental value, strengthening relationships. Simple DIY projects can be tailored to the recipient's tastes and needs, from jewelry holders to decorative planters. Wrapping gifts in reusable cloth or recycled paper adds an eco-friendly touch. Making gifts yourself reduces packaging waste and supports slow consumerism. These projects encourage skills like sewing, painting, or crafting, which can be shared during gift-making gatherings. Giving upcycled presents spreads awareness about sustainability in a joyful way. Thoughtful, sustainable gifting celebrates creativity and environmental responsibility while delighting friends and family."
        }
    },
    {
        "blog": {
            "title": "Trash to Treasure",
            "content": "Sometimes the best materials are the ones we throw away. Learn how to spot and transform trash into useful treasures.",
            "image": "blogs/trash_treasure.jpg",
            "author": "Charlie",
            "category_name": "Upcycling",
            "subtitle": "From Discarded to Desired",
            "body": "Upcycling trains your eye to see potential in the discarded. Cardboard, bottles, and broken items can become decor, storage, or art. For example, glass bottles transform into lamps or vases. Cardboard boxes become organizers or kids' toys with a little cutting and coloring. Broken furniture parts can be salvaged for shelving or frames. This approach reduces landfill and sparks innovation. Trash to treasure projects often require creativity, patience, and resourcefulness but are deeply satisfying. They encourage you to look beyond initial appearances and value materials differently. Community swaps or repair cafes provide venues to learn and share ideas. Through this mindset shift, waste becomes raw material, fostering sustainability and economic savings. Embracing trash to treasure supports environmental stewardship while unlocking artistic expression."
        }
    },
    {
        "blog": {
            "title": "2025 Fashion Forecast",
            "content": "Stay ahead of the curve with a look at the top fashion trends predicted to take over 2025.",
            "image": "blogs/fashion_forecast_2025.jpg",
            "author": "Bob",
            "category_name": "Trends",
            "subtitle": "What's Next in Style",
            "body": "Expect to see oversized silhouettes, earthy tones, and tech-integrated pieces. Sustainability remains central, with brands focusing on transparency and ethics. Designers increasingly incorporate recycled fabrics and biodegradable materials. Statement outerwear and exaggerated shapes dominate runways, blending comfort and boldness. Earthy colors like terracotta, olive, and sand convey connection to nature. Wearable technology advances with garments that monitor health or adapt temperature, merging utility with style. Minimalism coexists with maximalism, giving consumers choice and variety. Vintage influences blend with futuristic details, creating eclectic but cohesive collections. The rise of gender-neutral fashion continues, emphasizing self-expression over tradition. Consumers seek authenticity, valuing craftsmanship and stories behind garments. As fashion embraces circular economy principles, renting, repairing, and reselling gain popularity. 2025's trends reflect a fashion industry evolving toward responsibility, creativity, and innovation."
        }
    },
    {
        "blog": {
            "title": "Tech Meets Style",
            "content": "Fashion and technology are merging more than ever. Discover the latest innovations in wearable tech.",
            "image": "blogs/tech_fashion.jpg",
            "author": "Edward",
            "category_name": "Trends",
            "subtitle": "The Future Is Fashionable",
            "body": "From fitness-tracking shoes to temperature-regulating fabrics, fashion is evolving. These innovations bring both style and function into everyday wear. Smart textiles can adjust breathability or color based on environment or mood. Integrated sensors monitor biometrics like heart rate or UV exposure. 3D printing allows custom fits and complex designs impossible with traditional methods. Virtual fashion, worn in digital spaces, expands how people express identity. Brands collaborate with tech companies to create collections blending aesthetics and gadgets seamlessly. This fusion promotes wellness and convenience while maintaining trendiness. Fashion tech also reduces waste by enabling made-to-order garments and recycling fabrics efficiently. As technology advances, the line between clothing and wearable devices blurs, opening new frontiers for creativity and utility. Staying informed about these trends offers exciting possibilities for personal style and innovation."
        }
    },
    {
        "blog": {
            "title": "Color of the Season",
            "content": "Discover the trending colors dominating runways and street style this year—and how to wear them.",
            "image": "blogs/season_colors.jpg",
            "author": "Alice",
            "category_name": "Trends",
            "subtitle": "Shades of the Moment",
            "body": "Sage green and terracotta are in, offering a balance of calm and warmth. These hues are easy to pair and flatter almost every skin tone. Sage brings a fresh, herbal vibe perfect for spring and summer, while terracotta's earthy richness suits autumn and winter. Designers use these colors in varied textures, from soft knits to sleek silks, enhancing their versatility. Accessories in these tones complement neutrals like beige, cream, or charcoal. Wearing seasonal colors connects you to nature's cycles and can influence mood positively. Mixing shades of the season creates harmonious and on-trend looks without overwhelming the senses. These palettes encourage sustainable thinking by embracing colors found in the environment, supporting eco-conscious fashion. Experimenting with seasonal shades refreshes your wardrobe and keeps your style current and vibrant."
        }
    },
    {
        "blog": {
            "title": "Gender-Neutral Fashion",
            "content": "The future of fashion is inclusive. Learn how genderless fashion is reshaping the industry.",
            "image": "blogs/gender_neutral.jpg",
            "author": "Bella",
            "category_name": "Trends",
            "subtitle": "Style Without Labels",
            "body": "Neutral tones, loose fits, and unisex cuts are gaining traction. Fashion is becoming more about expression and less about category. Gender-neutral collections offer comfortable, versatile pieces that anyone can wear confidently. Designers focus on adaptable sizing and minimalist designs that suit varied bodies. This shift challenges traditional binaries and fosters inclusivity in the fashion industry. Accessories and styling emphasize individuality, allowing each person to interpret looks their own way. Retailers respond with sections dedicated to genderless clothing and marketing that avoids stereotypes. Consumers appreciate the freedom to explore styles beyond societal expectations. Gender-neutral fashion encourages diversity, acceptance, and innovation, reflecting broader cultural changes. Embracing this trend opens up creative possibilities and helps dismantle outdated norms in how we dress and present ourselves."
        }
    },
    {
        "blog": {
            "title": "Vintage Revival",
            "content": "Retro styles are back! From Y2K to '90s grunge, see how past trends are shaping today's looks.",
            "image": "blogs/vintage_revival.jpg",
            "author": "Charlie",
            "category_name": "Trends",
            "subtitle": "Old Is the New New",
            "body": "Vintage clothing isn't just nostalgic—it's sustainable. Thrift shopping and vintage-inspired design bring authenticity and environmental awareness to modern fashion. Past trends from the '90s grunge to Y2K's bold aesthetics influence current collections. Wearing vintage reduces demand for new production, lowering resource consumption and waste. Unique pieces add character to wardrobes, allowing personal storytelling through style. Many designers reinterpret vintage motifs with contemporary twists, blending old and new seamlessly. This revival promotes slow fashion, encouraging thoughtful purchases and garment care. Vintage shops often support local economies and communities. Collectors and fashion enthusiasts celebrate the craftsmanship and history behind older garments. Embracing vintage is both a style statement and an ethical choice, connecting past and present while paving the way for a greener fashion future."
        }
    }
]


def insert_blogs(blogs_data):
    for item in blogs_data:
        blog_data = item['blog']

        category_name = blog_data['category_name']
        category, _ = BlogCategory.objects.get_or_create(name=category_name)

        blog = Blog.objects.create(
            title=blog_data['title'],
            content=blog_data['content'],
            image=blog_data['image'],  # image already uploaded to this path
            author=blog_data['author'],
            category=category
        )

        BlogDetail.objects.create(
            blog=blog,
            subtitle=blog_data['subtitle'],   # extracted from blog_data
            body=blog_data['body']             # extracted from blog_data
        )

    print("Blog and BlogDetail entries added successfully.")


# Call the function with data

# insert_blogs(blogs_data)
