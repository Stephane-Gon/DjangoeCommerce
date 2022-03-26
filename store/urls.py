from os import name
from django.urls import path
from django.urls.resolvers import URLPattern
from .views import *

app_name= 'store'
urlpatterns = [
    path('', home_view, name='home'),
    path('contact/', contact_us_view, name='contact'),
    path('about/', About_view.as_view(), name="about"),
    path('gallery/', gallery_view, name='gallery'),
    path('gallery/slide/<slug:imgUrl>/', gallery_slide_view, name='gallery-slide'),
    path('categories/', Categories_view.as_view(), name='categories'),
    path('categories/single/<categorie>/', single_categorie_view, name='single-categorie'),
    path('product/<slug>/', product_view, name='product'),
    path('cart/', cart_view, name='cart'),
    path('update/', update_cart_view, name='update'),
    path('checkout/', checkout_view, name='checkout'),
    path('checkUser/', check_user_view, name='check-user'),
    path('process-order/', processOrder, name='process-order')
]