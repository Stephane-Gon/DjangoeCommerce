from django.contrib import admin
from .models import (
    Item,
    OrderItem,
    Order,
    Address,
    Categorie,
    Image,
    RefundedItems,
    Review,
    Transaction
)

def make_refund_accepted(modelAdmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)
make_refund_accepted.short_description = 'Update Orders to refund granted'


class ImageInline(admin.StackedInline):
    model = Image
    extra = 0

class RefundedItemsInline(admin.StackedInline):
    model = RefundedItems
    extra = 0

class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0

class ReviewInline(admin.StackedInline):
    model = Review
    extra = 0

class TransactionInline(admin.StackedInline):
    model = Transaction
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline, TransactionInline, RefundedItemsInline]

    list_display = [
        'id',
        'user',
        'ordered',
        'being_delivered',
        'received',
        'billing_address',
        'shipping_address',
    ]

    list_display_links = [
        'user',
        'billing_address',
        'shipping_address',
    ]

    list_filter = [
        'ordered',
        'being_delivered',
        'received',
    ]

    search_fields = [
        'user__username',
        'user__email',
        'id'
    ]

    actions = [make_refund_accepted]

class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'street_address',
        'apartment_address',
        'city',
        'state',
        'country',
        'zip',
        'address_type',
        'default'
    ]

    list_filter = [
        'address_type',
        'default',
        'country',
        'city',
        'state'
    ]

    search_fields = [
        'user__username',
        'street_address',
        'city',
        'state',
        'country',
        'zip'
    ]

class OrderItemAdmin(admin.ModelAdmin):
    inlines = [RefundedItemsInline]

    list_display = [
        'id',
        'refund_requested',
        'refund_granted',
        'item',
        'order',
        'quantity'
    ]
    search_fields = [
        'item__title',
        'id'
    ]
    list_filter = [
        'refund_requested',
        'refund_granted'
    ]

class ItemAdmin(admin.ModelAdmin):

    inlines = [ImageInline, ReviewInline]
    
    list_display = [
        'title',
        'id',
        'price',
        'stock'
    ]
    search_fields = [
        'title',
        'id'
    ]
    list_filter = [
        'stock'
    ]

class RefundedItemsAdmin(admin.ModelAdmin):
    list_display = [
        'order',
        'item',
    ]
    search_fields = [
        'item__item__title'
    ]

class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'order',
        'method',
    ]

admin.site.register(Item, ItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Categorie)
admin.site.register(Image)
admin.site.register(Review)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(RefundedItems, RefundedItemsAdmin)

