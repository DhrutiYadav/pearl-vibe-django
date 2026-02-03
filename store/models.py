from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self): return self.name


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    class Meta:
        verbose_name_plural = "Sub Categories"

    def __str__(self): return self.name


def default_sizes():
    return ["Free"]

class Product(models.Model):
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    price = models.FloatField()
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    digital = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    # ✅ ADD THESE TWO LINES
    colors = models.JSONField(default=list, blank=True)  # multiple colors
    # sizes = models.JSONField(default=default_sizes, blank=True)
    sizes = models.JSONField(default=default_sizes, blank=True)
    # default_color = models.CharField(max_length=20, default="#8B4513")

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            return self.image.url
        except:
            return ''


# -------------------------
# CART MODELS (REQUIRED)
# -------------------------

class Customer(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    contact_no = models.CharField(max_length=15, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name if self.name else str(self.user)


class Order(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for item in orderitems:
            if item.product.digital is False:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)
    size = models.CharField(max_length=20, blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)

    @property
    def get_total(self):
        return self.product.price * self.quantity


class ShippingAddress(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        null=True
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.SET_NULL,
        null=True
    )
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address


# -------------------------
# ORDER SUMMARY MODEL
# -------------------------
class OrderSummary(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="summary")
    subtotal = models.FloatField(default=0)
    tax = models.FloatField(default=0)
    shipping_cost = models.FloatField(default=0)
    total = models.FloatField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Summary for Order #{self.order.id}"


# -------------------------
# INVOICE MODEL
# -------------------------
class Invoice(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="invoice")
    invoice_number = models.CharField(max_length=100, unique=True)
    issued_date = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=True)

    def __str__(self):
        return f"Invoice {self.invoice_number}"
