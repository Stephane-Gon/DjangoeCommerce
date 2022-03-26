import json
import datetime

from django.conf import settings
from django.utils.html import strip_tags
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.views.generic import TemplateView, ListView
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .forms import ContactUsForm, AddReviewForm, OrderReplicaForm
from .models import Categorie, Item, Image, Review, OrderItem, Address, Order, Transaction
from users.forms import UserAddressInfoForm
from joaoLina.helpers import cartData, createOrder, getUserWidth
from joaoLina.settings.dev import SHIPPING_PRICE


# THIS IS THE ABOUT VIEW
class About_view(TemplateView):
    template_name = 'store/about_us.html'

    def get_context_data(self, **kwargs):
        dataCart = cartData(self.request)
        context = super(About_view, self).get_context_data(**kwargs)
        context['cartItems'] = dataCart['cartItems']
        return context

# THIS IS THE CATEGORIES VIEW
class Categories_view(ListView):
    template_name='store/categories.html'
    model = Categorie

    def get_context_data(self, **kwargs):
        dataCart = cartData(self.request)
        context = super(Categories_view, self).get_context_data(**kwargs)
        context['cartItems'] = dataCart['cartItems']
        return context


# THIS IS THE HOMEPAGE VIEW
def home_view(request):
    dataCart = cartData(request)

    request.user.userWidth =  getUserWidth(request)
    
    categories = Categorie.objects.get_queryset()
    items = Item.objects.all().exclude(tag = 'O')[:9]

    all_images = Image.objects.filter(image__icontains='landscape').order_by('?')[:9]

    context = {
        'categories' : categories,
        'items' : items,
        'cartItems': dataCart['cartItems'],
        'allImages' : all_images
    }

    return render(request, 'store/home_page.html', context)

# THIS IS THE CONTACT PAGE VIEW
def contact_us_view(request):
    dataCart = cartData(request)

    # HERE I GET THE USER WIDTH
    userWidth =  getUserWidth(request)

    form = ContactUsForm()
    if request.user.is_anonymous:
        form.fields['email'].required = True
    
    if request.method == 'POST':
        form  = ContactUsForm(request.POST or None)

        if form.is_valid():
            title = form.cleaned_data['title']
            subject = form.cleaned_data['subject']
            text = form.cleaned_data['text']
            email = None
            if request.user.is_anonymous:
                email = form.cleaned_data['email']
            else:
                email = request.user.email

            # HERE I SEND EMAIL TO THE SITE WITH THE USER CONTACT
            html_content_site = render_to_string('store/contact_us_template.html', {
                'user': request.user,
                'subject': subject,
                'text': text,
                'title': title,
                'email': email
            }) 
            plain_message_site = strip_tags(html_content_site)

            emailName =  f'Contacto de User: {request.user.username}'
            if request.user.is_anonymous:
                emailName = f'Contacto de User: Anónimo'

            email_site = EmailMultiAlternatives(
                emailName,
                plain_message_site,
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER]
            )
            email_site.attach_alternative(html_content_site, 'text/html')
            email_site.mixed_subtype = 'related'
            email_site.send()

            messages.success(request, f"You'r email was successfully delivered")
            return redirect('../contact/')


    context = {
        'form' : form,
        'cartItems': dataCart['cartItems']
    }
    if userWidth >= 1366:
        return render(request, 'store/contact_us.html', context)
    elif userWidth < 1366:
        return render(request, 'store/phone_contact_us.html', context)
    

# THIS IS THE GALLERY VIEW
def gallery_view(request):
    dataCart = cartData(request)
  
    test_img =  Image.objects.all().order_by('?')[:40]

    context = {
        'cartItems': dataCart['cartItems'],
        'testImg' : test_img
    }

    return render(request, 'store/gallery.html', context)

# THIS IS THE GALLERY WITH SLIDE VIEW
def gallery_slide_view(request, imgUrl):
    dataCart = cartData(request)

    first_img = Image.objects.filter(image__icontains=imgUrl)
    test_imgs =  Image.objects.all().exclude(image__icontains=imgUrl).order_by('?')[:39]

    all_imgs = []
    all_imgs.append(first_img[0].image.url)
    
    for img in test_imgs:
        all_imgs.append(img.image.url)
    
    context = {
        'images' : all_imgs,
        'cartItems': dataCart['cartItems']
    }
    return render(request, 'store/gallery_slide.html', context)

# THIS IS THE SINGLE CATEGORIE VIEW
def single_categorie_view(request, categorie):
    dataCart = cartData(request)

    all_categories = Categorie.objects.all()

    cat = get_object_or_404(Categorie, categorie = categorie)

    # HERE I GET ALL THE ITEMS FROM THIS CATEGORIE AND ATACH TO THEM THE RATING AVERAGE
    items = Item.objects.filter(categorie = cat)
    for item in items:
        item_reviews = item.reviews.all()
        if len(item_reviews) >= 1:
            rating = 0
            for review in item_reviews:
                rating += review.stars
            item.rating = round(rating/len(item_reviews))
        item.reviewsLen = len(item_reviews)

    item_paginator = Paginator(items, 6)
    page_num = request.GET.get('page')
    page = item_paginator.get_page(page_num)


    context = {
        'pageTotal': item_paginator.num_pages,
        'categorie': categorie,
        'page': page,
        'allCat': all_categories,
        'cartItems': dataCart['cartItems']
    }
    return render(request, 'store/single_categorie.html', context)

# THIS IS THE PRODUCT VIEW
def product_view(request, slug):
    dataCart = cartData(request)

    reviewForm = AddReviewForm()
    replicaForm = OrderReplicaForm()

    # HERE I GET THE CURRENT ITEM AND ALL HIS IMAGES
    item = get_object_or_404(Item, slug = slug)

    checkDate = datetime.datetime.now() - item.date_added.replace(tzinfo = None)

    if item.stock > 3 and item.tag == 'O':
        item.tag = ''
    if item.stock == 0 and item.tag == 'L':
        item.tag = 'O'
    if not item.discount_price and item.tag == 'S':
        item.tag = ''
    if checkDate.days > 30 and item.tag == 'N':
        item.tag = ''
    item.save()


    # HERE I GET THE CURRENT USER REVIEWS ON THIS ITEM AND CHECK IF THE USER BOUGHT THIS PRODUCT
    if request.user.is_authenticated:
        currentUserReview = Review.objects.filter(user = request.user, item = item)

        userOrdersMade = Order.objects.filter(user = request.user, ordered=True)
        userBoughtItem = OrderItem.objects.filter(item = item, order__in = userOrdersMade)
    else:
        currentUserReview = []
        userBoughtItem = []

    
    # HERE I APPEND THE MAIN IMAGE AND THE OTHER ONES TO THE SAME LIST
    sec_images = Image.objects.filter(item = item)
    all_images = []
    all_images.append(item.main_image)
    if len(sec_images) >= 1:
        all_images.extend(img.image for img in sec_images)


    # HERE I GET ALL THE REVIEWS FOR THE CURRENT ITEM
    reviews = item.reviews.all()

    # HERE I CALCULATE THE AVERAGE RATING OF THE CURRENT ITEM
    if len(reviews) >= 1:
        rating = 0
        for review in reviews:
            rating += review.stars
        item.rating = round(rating/len(reviews))

    # HERE I GET 3 ITEMS FROM THE SAME CATEGORIE OF THE CURRENT ONE
    identicalItems = Item.objects.filter(categorie = item.categorie).exclude(Q(id = item.id) | Q(tag = 'O'))[: 3]

    context = {
        'item': item,
        'images': all_images,
        'reviews': reviews,
        'form': reviewForm,
        'form2': replicaForm,
        'madeReview' : currentUserReview,
        'boughtItem' : userBoughtItem,
        'moreItems' : identicalItems,
        'cartItems': dataCart['cartItems']
    }

    if request.method == 'POST':
        reviewForm = AddReviewForm(request.POST or None)
        replicaForm = OrderReplicaForm(request.POST or None)

        if reviewForm.is_valid():
            # HERE I SAVE THE NEW REVIEW TO THE DB
            newReview = reviewForm.save(commit=False)
            newReview.user = request.user
            newReview.item = item
            newReview.save()

            messages.success(request, f"You'r review was made!")
            return redirect('store:product', slug = item.slug)
        
        if replicaForm.is_valid():
            replicaQuantity = replicaForm.cleaned_data['quantity']

            orderItem, created = OrderItem.objects.get_or_create(
                order = dataCart['order'],
                item = item,
                replica = True
	        )
            orderItem.quantity += int(replicaQuantity)
            orderItem.save()

            messages.success(request, f"You'r order was made!")
            return redirect('store:product', slug = item.slug)

        else:
            messages.error(request, f"You'r order was not made!")

    return render(request, 'store/product.html', context)


# THIS IS THE CART VIEW
def cart_view(request):
    dataCart = cartData(request)
    cartItems = dataCart['cartItems']
    order = dataCart['order']
    items = dataCart['items']

    context = {
        'cartItems': cartItems,
        'order' : order,
        'items' : items,
    }
    return render(request, 'store/cart.html', context)


# THIS IS THE ADD TO CART VIEW
def update_cart_view(request):
    data = json.loads(request.body)
    itemId = data['productId']
    action = data['action']
    message = ''
    # HERE I GET THE ITEM
    item = Item.objects.get(id=itemId)

    # HERE I GET OR CREATE AN ORDER AND ORDERITEM
    order = createOrder(request.user)
    
    data = {
        'itemId': item.id,
        'itemQuantity' : 0,
        'itemTotal' : 0,
    }

    replicaItem = {}

    try:
        replicaItem = OrderItem.objects.get(order=order, item=item)
    except:
        replicaItem['replica'] = False

    if item.stock == 0 and not replicaItem.replica:
        message = f'There is not enough stock of this item.'
    else:
        orderItem, created = OrderItem.objects.get_or_create(order=order, item=item)

        # HERE I CHECK IF THE QUANTITY WILL NOT PASS THE ITEM STOCK THEN,
        # I UPDATE THE QUANTITY OF THE ORDERITEM AND I SAVE/DELETE IT
        if action == 'add' and orderItem.replica and (orderItem.quantity + 1) > 10:
            message = f'You can only order 10 replicas'
        elif action == 'add' and (orderItem.quantity + 1) > item.stock and not orderItem.replica:
            message = f'There is not enough stock of this item.'
        elif action == 'add':
            orderItem.quantity = (orderItem.quantity + 1)
            message = f'The item {orderItem.item.title} was added to your cart.'
        elif action == 'remove':
            orderItem.quantity = (orderItem.quantity - 1)
            message = f'The item {orderItem.item.title} was subtracted from your cart.'
        orderItem.save()
        

        if orderItem.quantity <= 0 or action == 'delete':
            message = f"The item {orderItem.item.title} was removed from you'r cart."
            orderItem.delete()
        
        querySetItem = OrderItem.objects.filter(order=order, item=item)
        if len(querySetItem) != 0:
            data['itemQuantity'] = querySetItem[0].quantity
            data['itemTotal'] = querySetItem[0].get_total_price
    
    data['cartItems'] = order.get_cart_items
    data['message'] = message
    data['order_total'] = order.get_cart_total
    data['order_subTotal'] = order.get_cart_subTotal
    data['order_shipping'] = order.get_total_shipping
    return JsonResponse(dict(data), safe=False)


# THIS FUNCTION DEALS WITH THE CHECKOUT PROCESS
def check_user_view(request):
    if request.user.is_anonymous:
        messages.warning(request, 'You need an account to checkout.')
        return redirect('../../register')

    dataCart = cartData(request)
    cartItems = dataCart['cartItems']
    if cartItems == 0:
        messages.warning(request, "You don't have any items in your cart.")
        return redirect('../../cart')

    return checkout_view(request)


@login_required
def checkout_view(request):
    dataCart = cartData(request)
    cartItems = dataCart['cartItems']
    order = dataCart['order']
    items = dataCart['items']
    
    user = request.user
    
    shippingAddress = Address.objects.get(user = user, address_type = 'S') 
    userSForm = UserAddressInfoForm(instance = shippingAddress, prefix="form1")
    
    billingAddress = Address.objects.get(user = user, address_type = 'B')
    userBForm = UserAddressInfoForm(instance=billingAddress, prefix="form2")

    context = {
        'cartItems': cartItems,
        'order' : order,
        'items' : items,
        'sForm' : userSForm,
        'bForm' : userBForm,
        'userAddress': shippingAddress
    }

    if request.method == 'POST':
        userSForm = UserAddressInfoForm(request.POST, prefix="form1")
        userBForm = UserAddressInfoForm(request.POST, prefix="form2")

        if 'user-shipping-form' in request.POST and  userSForm.is_valid():
            shippingAddress.street_address = userSForm.cleaned_data['street_address']
            shippingAddress.apartment_address = userSForm.cleaned_data['apartment_address']
            shippingAddress.city = userSForm.cleaned_data['city']
            shippingAddress.state = userSForm.cleaned_data['state']
            shippingAddress.zip = userSForm.cleaned_data['zip']
            shippingAddress.country = userSForm.cleaned_data['country']
            shippingAddress.save()

        if 'user-billing-form' in request.POST and userBForm.is_valid():
            billingAddress.street_address = userBForm.cleaned_data['street_address']
            billingAddress.apartment_address = userBForm.cleaned_data['apartment_address']
            billingAddress.city = userBForm.cleaned_data['city']
            billingAddress.state = userBForm.cleaned_data['state']
            billingAddress.zip = userBForm.cleaned_data['zip']
            billingAddress.country = userBForm.cleaned_data['country']
            billingAddress.save()
        
        return redirect('store:checkout')

    return render(request, 'store/checkout.html', context)


# THIS FUNCTIONS DEALS WITH THE ORDER PROCESS
@login_required
def processOrder(request):
    data = json.loads(request.body)

    transaction = data['transaction']
    order = createOrder(request.user)
    orderItems = OrderItem.objects.filter(order=order)
    

    # HERE I CHECK IF THE TOTAL VALUE FROM THE FRONTEND IS THE SAME FROM THE BACKEND
    
    if float(data['total']) != float(order.get_cart_total):
        messages.error(request, 'Something went wrong with your checkout.')
        return redirect('store:checkout')
    
    # HERE SINCE I CHANGE THE .ORDERED TO TRUE, ON THE NEXT RELOAD A NEW ORDER WILL BE CREATED WITH .ORDERED == FALSE
    newDate = datetime.datetime.now()
    order.ordered = True
    order.being_delivered = True
    order.ordered_date = newDate
    order.refund_deadline = newDate + datetime.timedelta(30)
    order.old_shipping = SHIPPING_PRICE

    for i in orderItems:
        item = Item.objects.get(id= i.item.id)
        

        oItem = OrderItem.objects.get(item=item, order=order)
        oItem.old_price = item.price * (100 - item.discount_price) / 100
        oItem.save()

        if not oItem.replica:
            item.stock -= i.quantity
            if item.stock <= 3 and item.stock > 0:
                item.tag = 'L'
            elif item.stock <= 0:
                item.tag = 'O'
            item.save()
        
        # HERE I REMOVE ALL ORDERITEMS IN OTHER CARTS THAT HAD THEIR STOCK REDUCED AFTER THIS ORDER
        if item.stock <= 0:
            repeatedItems = OrderItem.objects.filter(item = item).exclude(order = order)
            for j in repeatedItems:
                if j.order.ordered == False:
                    OrderItem.objects.get(order = j.order, item = item).delete()
    
    orderItems = OrderItem.objects.filter(order=order)

    # HERE I CREATE A NEW TRANSACTION
    newTransaction = Transaction(
        order = order,
        email = transaction['email'],
        transaction_id = transaction['id'],
        method = transaction['method'],
        status = transaction['status'],
        date_added = transaction['date']
    )
    newTransaction.save()

    # HERE I SEND AN EMAIL TO THE USER
    html_content_user = render_to_string('store/order_sent_user_template.html', {
                'user': request.user,
                'order': order,
                'items': orderItems
            }) 
    plain_message_user = strip_tags(html_content_user)

    email_user = EmailMultiAlternatives(
        'Your order was sent',
        plain_message_user,
        settings.EMAIL_HOST_USER,
        [request.user.email]
    )
    email_user.attach_alternative(html_content_user, 'text/html')
    email_user.mixed_subtype = 'related'
    email_user.send()
    
    # HERE I SEND AN EMAIL TO THE SITE
    html_content_site = render_to_string('store/order_sent_site_template.html', {
                'user': request.user,
                'order': order,
                'items': orderItems,
                'transaction': transaction
            }) 
    plain_message_site = strip_tags(html_content_site)

    email_site = EmailMultiAlternatives(
        'Nova encomenda',
        plain_message_site,
        settings.EMAIL_HOST_USER,
        [settings.EMAIL_HOST_USER]
    )
    email_site.attach_alternative(html_content_site, 'text/html')
    email_site.mixed_subtype = 'related'
    email_site.send()

    order.save()
    return JsonResponse('Payment submitted..', safe=False)
