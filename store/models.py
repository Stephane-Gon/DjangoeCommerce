from django.utils.crypto import get_random_string


from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE, SET_NULL
from django.urls import reverse
from django.conf import settings
from django.utils.six import b
from django_countries.fields import CountryField

from users.models import UserAccount
from joaoLina.settings.dev import SHIPPING_PRICE
# from joaoLina.settings.prod import SHIPPING_PRICE



ADDRESS_CHOICES = (
    ('B', 'billing'),
    ('S', 'shipping'),
)

ITEM_TAGS = (
	('S', 'sale'),
	('N', 'new'),
	('L', 'limited'),
	('O', 'out')
)

class Categorie(models.Model):
	categorie = models.CharField(max_length=200, null=True, unique=True)
	image 	  = models.ImageField(null=True)

	def __str__(self):
		return self.categorie
	
	def get_absolute_url(self):
		return reverse("store:single-categorie", kwargs={
			'categorie': self.categorie	
		})


class Item(models.Model):
    title 		= models.CharField(max_length=100)
    price 		= models.DecimalField(max_digits=30, decimal_places=2)
    discount_price 	= models.DecimalField(default=0, max_digits=3, decimal_places=0)
    slug 		= models.SlugField(blank=True)
    description = models.TextField()
    categorie	= models.ForeignKey(Categorie, on_delete=SET_NULL, null=True, to_field='categorie', default='Diversos')
    main_image 	= models.ImageField()
    tag         = models.CharField(max_length=1, choices=ITEM_TAGS, null=True, blank=True, default='N')
    stock       = models.IntegerField()
    weight      = models.DecimalField(decimal_places=3, max_digits=20)
    dimensions  = models.CharField(blank=True, null=True, max_length=50)
    materials   = models.CharField(blank=True, null=True, max_length=200)
    craftsman   = models.CharField(blank=True, null=True, max_length=100)
    date_added  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("store:product", kwargs={
            'slug': self.slug
        })

    @property
    def get_discount_price(self):
        return self.price * (100 - self.discount_price) / 100

    # Add Slug creating/checking to save method. 
    def save(self, *args, **kwargs):
        slug_save(self)
        super(Item, self).save(*args, **kwargs)


class Image(models.Model):
	image 	  = models.ImageField(null=True)
	item      = models.ForeignKey(Item, on_delete=models.CASCADE, null=True)


class Order(models.Model):
	user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, null=True, blank=True)
	slug = models.SlugField(blank=True)
	ref_code = models.CharField(max_length=20, null=True, blank=True)
	ordered = models.BooleanField(default=False)
	start_date = models.DateTimeField(auto_now_add=True)
	ordered_date = models.DateTimeField(null=True, blank=True)
	billing_address = models.ForeignKey('Address', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
	shipping_address = models.ForeignKey('Address', related_name='shipping_address', on_delete=models.SET_NULL, null=True, blank=True)
	old_shipping = models.DecimalField(decimal_places=3, max_digits=20, blank=True, null=True)

	being_delivered = models.BooleanField(default=False)
	received = models.BooleanField(default=False)
	refund_deadline = models.DateTimeField(null=True, blank=True)

	def __str__(self):
		return str(self.id)
	
	def get_absolute_url(self):
		return reverse("order-details", kwargs= {
			'slug': self.slug
		})
	
	# Add Slug creating/checking to save method.  
	def save(self, *args, **kwargs): 
		slug_save(self)
		super(Order, self).save(*args, **kwargs)

	@property
	def get_cart_subTotal(self):
		orderItems = self.orderitem_set.all()
		total = sum([(item.item.price * (100 - item.item.discount_price) / 100) * item.quantity for item in orderItems])
		return total
	
	@property
	def get_cart_total(self):
		orderItems = self.orderitem_set.all()

		shipping_total = sum([item.item.weight * item.quantity for item in orderItems]) * SHIPPING_PRICE

		total = sum([(item.item.price * (100 - item.item.discount_price) / 100) * item.quantity for item in orderItems]) + shipping_total
		return "{:.2f}".format(total)

	@property
	def get_total_shipping(self):
		orderItems = self.orderitem_set.all()

		shipping_total = sum([item.item.weight * item.quantity for item in orderItems]) * SHIPPING_PRICE
		return "{:.2f}".format(shipping_total)
	
	@property
	def get_cart_items(self):
		orderItems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderItems])
		return total

	# THIS PROPERTIES ARE FOR ORDER DETAILS VIEW
	
	@property
	def get_old_cart_total(self):
		orderItems = self.orderitem_set.all()
		shipping_total = sum([item.item.weight * item.quantity for item in orderItems]) * self.old_shipping
		total = sum([item.old_price  * item.quantity for item in orderItems]) + shipping_total
		return "{:.2f}".format(total)

	@property
	def get_old_cart_subTotal(self):
		orderItems = self.orderitem_set.all()
		total = sum([item.old_price * item.quantity for item in orderItems])
		return total

	@property
	def get_old_total_shipping(self):
		orderItems = self.orderitem_set.all()

		shipping_total = sum([item.item.weight * item.quantity for item in orderItems]) * self.old_shipping
		return "{:.2f}".format(shipping_total)


class OrderItem(models.Model):
	order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
	item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	old_price = models.DecimalField(max_digits=30, decimal_places=2, blank=True, null=True)
	replica = models.BooleanField(blank=True, null=True, default=False)
	refund_requested = models.BooleanField(default=False)
	refund_granted = models.BooleanField(default=False)

	def __str__(self):
		return f'{self.quantity} of {self.item.title}'
	
	@property
	def get_total_price(self):
		return (self.item.price * (100 - self.item.discount_price) / 100) * self.quantity
	
	# THIS PROPERTIES ARE FOR ORDER DETAILS VIEW
	@property
	def get_old_total_price(self):
		return self.old_price  * self.quantity


class Address(models.Model):
	user = models.ForeignKey(UserAccount, related_name="address", on_delete=models.CASCADE, null=True)
	street_address = models.CharField(max_length=150, null=False)
	apartment_address = models.CharField(max_length=150, null=False)
	city = models.CharField(max_length=200, null=False)
	state = models.CharField(max_length=200, null=False)
	country = CountryField(multiple = False)
	zip = models.CharField(max_length=80)
	address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
	default = models.BooleanField(default=False)

	def __str__(self):
		return str(self.id)

	class Meta:
		verbose_name_plural = 'Addresses'


class Transaction(models.Model):
	order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
	email = models.EmailField(verbose_name='email', max_length=70, blank=True)
	transaction_id = models.CharField(max_length=60, blank=True)
	method = models.CharField(max_length=30, blank=True)
	status = models.CharField(max_length=50, blank=True)
	date_added  = models.DateTimeField()


	def __str__(self):
		return str(self.id)


class RefundedItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    item = models.ForeignKey(OrderItem, on_delete=models.CASCADE)
    reason = models.TextField()
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.pk}"

    @property
    def get_refund_total(self):
      total = self.item.old_price *  self.quantity
      return total


class Review(models.Model):
	content = models.TextField()
	user = models.ForeignKey(UserAccount, null=True, blank=True, on_delete=models.CASCADE)
	item = models.ForeignKey(Item, related_name="reviews",null=True, blank=True, on_delete=models.CASCADE)
	stars = models.IntegerField(null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.item.title


# FUNCTION THAT GENERATES RANDOM 8 CHAR SLUGS AND CHECKS IF IT IS UNIQUE
def slug_save(obj):

  if not obj.slug: # if there isn't a slug
    obj.slug = get_random_string(8) # create one
    slug_is_wrong = True  
    while slug_is_wrong: # keep checking until we have a valid slug
        slug_is_wrong = False
        other_objs_with_slug = type(obj).objects.filter(slug=obj.slug)
        if len(other_objs_with_slug) > 0:
            # if any other objects have current slug
            slug_is_wrong = True
        if slug_is_wrong:
            # create another slug and check it again
            obj.slug = get_random_string(8)