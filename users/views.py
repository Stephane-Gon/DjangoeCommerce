from django.utils import timezone
import datetime
import json
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.core.paginator import Paginator

from .forms import (
    UserRegisterForm, 
    UserLoginForm, 
    UserPersonalInfoForm, 
    UserAddressInfoForm, 
    UserChangePasswordForm,
    RefundItemForm,
)
from store.models import Address, Item, OrderItem, Order, RefundedItems, Transaction
from .models import UserAccount, TokenGenerator
from joaoLina.helpers import (
    getUserWidth,
    send_my_email, 
    login_forbidden, 
    cartData, 
    createOrder
)


@csrf_protect
@login_forbidden
def login_view(request):
    dataCart = cartData(request)
    lForm = UserLoginForm()
    rForm = UserRegisterForm()

    # HERE I GET THE USER WIDTH FROM THE COOKIES
    userWidth = getUserWidth(request)

    if request.method == 'POST':
        lForm = UserLoginForm(request.POST or None)
        if lForm.is_valid():

            email = lForm.cleaned_data['email']
            password = lForm.cleaned_data['password1']
            user = authenticate(email=email, password=password)

            if user != None and user.account_activated == True:
                login(request, user)

                messages.success(request, f"You logged in as  {user.username}!")
                return redirect('../')
            elif user != None and user.account_activated == False:
                account_activation_token = TokenGenerator()
                return redirect(f'../resend_activate_account/{urlsafe_base64_encode(force_bytes(user.pk))}/{account_activation_token.make_token(user)}')
            else:
                print('Error logging in User!')
                return redirect('../login/')  

    context = {
        'title': 'Login Page',
        'rForm': rForm,
        'lForm': lForm,
        'cartItems': dataCart['cartItems']
    }

    if userWidth >= 768:
        return render(request, 'users/login.html', context)
    elif userWidth < 768:
        return render(request, 'users/phone_login.html', context)

@login_required
def logout_view(request):
    logout(request)
    dataCart = cartData(request)
    return render(request, 'users/logout.html', {'cartItems': dataCart['cartItems']})

@csrf_protect
@login_forbidden
def register_view(request):
    dataCart = cartData(request)
    rForm = UserRegisterForm()
    lForm = UserLoginForm()

    # HERE I GET THE USER WIDTH FROM THE COOKIES
    userWidth = getUserWidth(request)

    if request.method == 'POST':
        rForm = UserRegisterForm(request.POST)

        if rForm.is_valid():
  
            user = rForm.save(commit=False)
            rForm.save()

            # HERE I SEND THE USER THE EMAIL TO ACTIVATE HIS NEW ACCOUNT
            send_my_email(request, user)

            token = TokenGenerator()
            context = {
                'message' : 'We have send you an email so you can activate your account.',
                'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : token
            }

            return render(request, 'users/verify_email.html', context)

    context = {
        'title': 'Register Page',
        'rForm' : rForm,
        'lForm': lForm,
        'cartItems': dataCart['cartItems']
    }
    if userWidth >= 768:
        return render(request, 'users/login.html', context)
    elif userWidth < 768:
        return render(request, 'users/phone_login.html', context)


def activate_view(request, uidb64, token):
    dataCart = cartData(request)
    User = get_user_model()
    account_activation_token = TokenGenerator()
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.account_activated = True
        user.save()

        shippingAddress, created = Address.objects.get_or_create(
            user = user,
            address_type = 'S'
        )
        shippingAddress.save()

        billingAddress, created = Address.objects.get_or_create(
            user = user,
            address_type = 'B'
        )
        billingAddress.save()

        cartCookie = json.loads(request.COOKIES['cart'])

        if cartCookie != {}:
            order = createOrder(user)
            for i in cartCookie:
                product = Item.objects.get(id=i)
                quantity = cartCookie[i]['quantity']
                orderItem, created = OrderItem.objects.get_or_create(order=order, item=product, quantity=quantity)

        context = {
            'message' : "Thank's for verifying your email. You can now login to your account.",
            'title' : 'Email Verified',
            'active': True,
            'cartItems': dataCart['cartItems']
        }
        messages.success(request, f"You created an account as {user.username}!")

        # ============== QUANDO ESTIVER ONLINE TROCAR AQUI O "domain=";
        response = render(request, 'users/verified_email.html', context)
        response.delete_cookie('cart', domain='joaolina.herokuapp.com')
    else:
        context = {
            'message' : 'Activation link is invalid!',
            'title' : 'Email Not Verified',
            'active': False,
            'uidb64': uidb64,
            'token' : token,
            'cartItems': dataCart['cartItems']

        }
        response = render(request, 'users/verified_email.html', context)
    return response


def send_activateEmail_view(request, uidb64, token):
    dataCart = cartData(request)
    uid = force_text(urlsafe_base64_decode(uidb64))
    user = UserAccount.objects.get(pk = uid)
    send_my_email(request, user)

    context = {
        'message': "You'r account is not activated so we sended you another email so you can verify it.",
        'uidb64' : uidb64,
        'token' : token,
        'cartItems': dataCart['cartItems']
    }
    return render(request, 'users/verify_email.html', context)


@login_required
def user_account_view(request):
    dataCart = cartData(request)

    user = request.user

    # HERE I SEND THE USER WIDTH IN THE REQUEST
    request.user.userWidth =  getUserWidth(request)

    userInfoForm = UserPersonalInfoForm(instance = user)
    userPassForm = UserChangePasswordForm(user)

    shippingAddress = Address.objects.get(user = user, address_type = 'S') 
    userSForm = UserAddressInfoForm(instance = shippingAddress, prefix="form1")

    billingAddress = Address.objects.get(user = user, address_type = 'B')
    userBForm = UserAddressInfoForm(instance=billingAddress, prefix="form2")

    orders = Order.objects.filter(user = user, ordered = True).order_by('-ordered_date')

    # HERE I PAGINATE THE ORDERS
    item_paginator = Paginator(orders, 6)
    page_num = request.GET.get('page')
    page = item_paginator.get_page(page_num)

    context = {
        'pageTotal': item_paginator.num_pages,
        'title' : 'User Account',
        'page': page,
        'userInfoForm' : userInfoForm,
        'userBForm' : userBForm,
        'userSForm' : userSForm,
        'userPassForm': userPassForm,
        'userInfo' : user,
        'userS' : shippingAddress,
        'userB': billingAddress,
        'cartItems': dataCart['cartItems']
    }

    if request.method == 'POST':
        userSForm = UserAddressInfoForm(request.POST, prefix="form1")
        userInfoForm = UserPersonalInfoForm(request.POST)
        userBForm = UserAddressInfoForm(request.POST,  prefix="form2")
        userPassForm = UserChangePasswordForm(data=request.POST, user=user)
        
        # CHECKS USER INFO FORM
        if 'user-info-form' in request.POST and userInfoForm.is_valid():
            firstName = userInfoForm.cleaned_data['first_name'].strip()
            lastName = userInfoForm.cleaned_data['last_name'].strip()

            user.last_name = lastName
            user.first_name = firstName

            user.save()
            messages.success(request, 'You updated your personal information successfully!')

            context['title'] = 'Update Info'
            context['userInfoForm'] = userInfoForm
            return render(request, 'users/user_account.html', context)

        elif 'user-info-form' in request.POST and userInfoForm.is_valid() == False:
            context['title'] = 'Update Info'
            context['userInfoForm'] = userInfoForm
            return render(request, 'users/user_account.html', context)
        
        # CHECHS THE USER PASSWORD FORM
        if 'user-pass-form' in request.POST and userPassForm.is_valid():

            userPassForm.save()
            update_session_auth_hash(request, userPassForm.user)

            context['title'] = 'Update Info'

            messages.success(request, 'You updated your password successfully!')
            return render(request, 'users/user_account.html', context)

        elif 'user-pass-form' in request.POST and userPassForm.is_valid() == False:
            context['title'] = 'Update Info'
            context['userPassForm'] = userPassForm
            return render(request, 'users/user_account.html', context)

        # CHECKS USER SHIPPING ADDRESS FORM
        if 'user-shipping-form' in request.POST and userSForm.is_valid():

            shippingAddress.street_address = userSForm.cleaned_data['street_address']
            shippingAddress.apartment_address = userSForm.cleaned_data['apartment_address']
            shippingAddress.city = userSForm.cleaned_data['city']
            shippingAddress.state = userSForm.cleaned_data['state']
            shippingAddress.zip = userSForm.cleaned_data['zip']
            shippingAddress.country = userSForm.cleaned_data['country']

            shippingAddress.save()

            messages.success(request, 'You updated your shipping address successfully!')
            context['title'] = 'Update Info'
            context['userSForm'] = userSForm
            return render(request, 'users/user_account.html', context)

        elif 'user-shipping-form' in request.POST and userSForm.is_valid() == False:
            context['title'] = 'Update Info'
            context['userSForm'] = userSForm
            return render(request, 'users/user_account.html', context)

        # CHECKS USER BILLING ADDRESS FORM
        if 'user-billing-form' in request.POST and userBForm.is_valid():
            billingAddress.street_address = userBForm.cleaned_data['street_address']
            billingAddress.apartment_address = userBForm.cleaned_data['apartment_address']
            billingAddress.city = userBForm.cleaned_data['city']
            billingAddress.state = userBForm.cleaned_data['state']
            billingAddress.zip = userBForm.cleaned_data['zip']
            billingAddress.country = userBForm.cleaned_data['country']

            billingAddress.save()

            messages.success(request, 'You updated your billing address successfully!')
            context['title'] = 'Update Info'
            context['userBForm'] = userBForm
            return render(request, 'users/user_account.html', context)
        
        elif 'user-billing-form' in request.POST and userBForm.is_valid() == False:
            context['title'] = 'Update Info'
            context['userBForm'] = userBForm
            return render(request, 'users/user_account.html', context)
    
    return render(request, 'users/user_account.html', context)


@login_required
def order_details_view(request, slug):
    dataCart = cartData(request)
    try:
        order = Order.objects.get(slug = slug, user = request.user)
    except:
        messages.error(request, f'This is not your order.')
        return redirect('/user_account/')

    transaction = Transaction.objects.get(order=order)

    # HERE I PREPARE THE REFUNDED ITEMS FORM
    form = RefundItemForm()

    order.refund_deadline = order.refund_deadline.astimezone(timezone.utc).replace(tzinfo=None)

    if request.method == 'POST':
        
        form = RefundItemForm(request.POST, request.FILES)

        # ASK REFUND FORM LOGIC
        if order.refund_deadline < datetime.datetime.now():
            messages.error(request, f'The refund deadline is already over.')
            return redirect(f'/order_details/{order.slug}/')
 
        if form.is_valid():
            # HERE I GET THE FORM INPUT'S VALUES
            reason = form.cleaned_data['reason'] 
            quantity = form.cleaned_data['quantity']
            itemId = form.cleaned_data['item']

            # HERE I GET THE ORDER ITEM
            orderItemRefund = OrderItem.objects.get(order=order, item = itemId)

            # HERE I CHECK IF THE USER PASSED A RIGHT AMMOUNT FOR THE QUANTITY
            if quantity > orderItemRefund.quantity:
                messages.error(request, f'You can only refund a maximum of {orderItemRefund.quantity} of this item.')
                return redirect(f'/order_details/{order.slug}/')
            elif quantity < 0:
                messages.error(request, f'You have to refund at least 1 of this item.')
                return redirect(f'/order_details/{order.slug}/')

            # HERE I CHEK IF THE USER SENT THE RIGHT AMMOUNT AND TYPE OF FILES
            if len(request.FILES.getlist('images')) > quantity * 2:
                messages.error(request, f'You can only send a maximum of {quantity * 2} images.')
                return redirect(f'/order_details/{order.slug}/')
            elif len(request.FILES.getlist('images')) < quantity:
                messages.error(request, f'You need to send at least one image per product.')
                return redirect(f'/order_details/{order.slug}/')
            else:
                for img in request.FILES.getlist('images'):
                    if img.content_type != 'image/png' and img.content_type != 'image/jpg' and img.content_type != 'image/jpeg':
                        messages.error(request, f'You can only send PNG, JPEG and JPG files.')
                        return redirect(f'/order_details/{order.slug}/')
            
            
            # HERE I UPDATE THE ORDER ITEM REFUND STATUS 
            orderItemRefund.refund_requested = True
            orderItemRefund.save()

            # HERE I CREATE A NEW REFUNDED ITEM INSTANCE
            refundedItem, created = RefundedItems.objects.get_or_create(
                order = order,
                item = orderItemRefund,
                reason = reason,
                quantity = quantity
            )
            refundedItem.save()
        
        
            # HERE I SEND AN EMAIL TO THE USER WITH THE REFUND STEPS
            html_content_user = render_to_string('users/refund_user_template.html', {
                        'user': request.user,
                        'refund' : refundedItem
                    }) 
            plain_message_user = strip_tags(html_content_user)
            email_user = EmailMultiAlternatives(
                'Refund asked',
                plain_message_user,
                settings.EMAIL_HOST_USER,
                [request.user.email]
            )
            email_user.attach_alternative(html_content_user, 'text/html')
            email_user.mixed_subtype = 'related'
            email_user.send()
        
        
            # HERE I SEND AN EMAIL TO THE SITE WITH THE REFUND STEPS
            html_content_user = render_to_string('users/refund_site_template.html', {
                        'user': request.user,
                        'refund' : refundedItem,
                        'transaction': transaction
                    }) 
            plain_message_user = strip_tags(html_content_user)
        
            email_user = EmailMultiAlternatives(
                'Devolução pedida',
                plain_message_user,
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER]
            )
            email_user.attach_alternative(html_content_user, 'text/html')
            email_user.mixed_subtype = 'related'
            for image in request.FILES.getlist('images'): 
                email_user.attach(image.name, image.read(), image.content_type)
            email_user.send()
        
        
            order.save()
            messages.success(request, f'Your refund for the items of the order {order.id} is being processed.')

    context = {
        'order': order,
        'form': form,
        'nowDate': datetime.datetime.now(),
        'cartItems': dataCart['cartItems'],
        'transaction': transaction
    }
    return render(request, 'users/order_details.html', context)


def cancel_refund_view(request, slug):
    try:
        order = Order.objects.get(slug = slug, user = request.user)
    except:
        messages.error(request, f'This is not your order.')
        return redirect('/user_account/')

    if request.POST:
        cancelItem = request.POST['cancel']
        if cancelItem != 'on':
            messages.error(request, f'You have to check the box in order to cancel the refund.')
            return redirect(f'/order_details/{order.slug}/')  
        
        itemId = request.POST['item']
        orderItem = OrderItem.objects.get(order = order, item = itemId)
            
        if orderItem.refund_requested == True:
            orderItem.refund_requested = not cancelItem
            orderItem.save()
            refund = RefundedItems.objects.get(order = order, item = orderItem)
                
            # HERE I SEND AN EMAIL TO THE SITE CANCELING THE REFUND
            html_content_user = render_to_string('users/refund_cancel_site_template.html', {
                        'user': request.user,
                        'refund': refund
                    }) 
            plain_message_user = strip_tags(html_content_user)

            email_user = EmailMultiAlternatives(
                'Devolução cancelada',
                plain_message_user,
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER]
            )
            email_user.attach_alternative(html_content_user, 'text/html')
            email_user.mixed_subtype = 'related'
            email_user.send()
            
            refund.delete()

            order.save()
            messages.success(request, f'You successfully canceled the refund of the item {orderItem.item.title}.')
    return redirect(f'/order_details/{order.slug}/')

