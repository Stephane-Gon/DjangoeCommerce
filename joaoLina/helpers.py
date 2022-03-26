import json

from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from users.models import TokenGenerator
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.decorators import user_passes_test

from store.models import *
from joaoLina.settings.base import SHIPPING_PRICE

# VER UMA FORMA DE SÓ PASSAR O VALOR DE CARTITEMS PARA VIEWS QUE NÃO PRECISÃO DE MAIS
def cookieCart(request):
	try:
		cart = json.loads(request.COOKIES['cart'])
	except:
		cart = {}

	items = []
	order = {
		'get_cart_total': 0, 
		'get_cart_items': 0,
		'get_cart_subTotal': 0,
		'get_total_shipping': 0
	}
	cartItems = order['get_cart_items']
	
	for i in cart:
		# I USED TRY BLOCK TO PREVENT ERRORS FROM ITEMS THAT MAY HAVE BEEN REMOVED FROM THE DB
		try:
			product = Item.objects.get(id=i)
			cartItems += cart[i]['quantity']
			shipping = ((product.weight * SHIPPING_PRICE) * cart[i]['quantity'])
			total = product.get_discount_price * cart[i]['quantity'] + shipping
			subTotal = (product.get_discount_price * cart[i]['quantity'])
			
			order['get_cart_total'] += total
			order['get_cart_items'] += cart[i]['quantity']
			order['get_cart_subTotal'] += subTotal
			order['get_total_shipping'] += shipping
			
			item = {
				'item': {
					'id': product.id,
					'title': product.title,
					'price': product.price,
					'discount_price': product.discount_price,
					'main_image': product.main_image,
					'get_absolute_url': product.get_absolute_url,
					'get_discount_price': product.get_discount_price
				},
				'quantity': cart[i]['quantity'],
				'get_total_price': product.get_discount_price * cart[i]['quantity']
			}
			items.append(item)
		except:
			item = None
			items.append(item)		

	return {'cartItems':cartItems ,'order':order, 'items':items}

def cartData(request):

	if request.user.is_authenticated:
		user = request.user

		order = createOrder(user)

		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		cookieData = cookieCart(request)
		cartItems = cookieData['cartItems']
		order = cookieData['order']
		items = cookieData['items']

	return {'cartItems':cartItems ,'order':order, 'items':items}


def createOrder(user):
	allAddress = user.address.all()
	for address in allAddress:
		if address.address_type == 'S':
			shipping_address = address
		elif address.address_type == 'B':
			billing_address = address

	order, created = Order.objects.get_or_create(
		user=user,
		ordered=False,
		shipping_address = shipping_address,
		billing_address = billing_address
	)
	return order


def send_my_email(request, user):
        account_activation_token = TokenGenerator()
        current_site = get_current_site(request)
        to_email = user.email
        
        html_content_site = render_to_string('users/verify_email_template.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        }) 
        plain_message_site = strip_tags(html_content_site)
        email_site = EmailMultiAlternatives(
            'Activate your account.',
            plain_message_site,
            settings.EMAIL_HOST_USER,
            [to_email]
        )
        email_site.attach_alternative(html_content_site, 'text/html')
        email_site.mixed_subtype = 'related'
        
        return email_site.send()


def login_forbidden(function=None, redirect_field_name=None, redirect_to='/'):
    
    actual_decorator = user_passes_test(
        lambda u: u.is_anonymous,
        login_url=redirect_to,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


# HERE I GET THE USER WIDTH FROM THE COOKIES
def getUserWidth(request):
	try:
		userWidth = json.loads(request.COOKIES['viewport'])
	except:
		userWidth = 1900
	return userWidth