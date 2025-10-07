from django.db import models

# In commerces you should have: Address: user’s saved delivery addresses. Address — a user’s saved delivery address (one user can have many addresses). Order — a purchase placed by a user for one restaurant and delivered to one address. Includes simple status (e.g., new/confirmed/delivering/done) and totals (subtotal, discount_total, total). OrderItem — a snapshot of a MenuItem inside the order (stores item name/price at the moment of purchase, plus quantity and line_total). OrderItemOption — selected options for each order item (stores option name and price_delta snapshot). PromoCode — a discount code (unique). OrderPromo (through-table) — many-to-many between Order and PromoCode, with extra applied_amount to record the actual discount used.

class Address(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='addresses')
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.street}, {self.city}, {self.state}, {self.zip_code}, {self.country}"
    
class PromoCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code
    
class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('confirmed', 'Confirmed'),
        ('delivering', 'Delivering'),
        ('done', 'Done'),
    ]

    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='orders')
    restaurant = models.ForeignKey('catalogs.Restaurant', on_delete=models.CASCADE, related_name='orders')
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    discount_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    promo_codes = models.ManyToManyField(PromoCode, through='OrderPromo', related_name='orders')

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    menu_item = models.ForeignKey('catalogs.MenuItem', on_delete=models.CASCADE)
    item_name = models.CharField(max_length=255)
    item_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    line_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.item_name} in Order {self.order.id}"
    
class OrderItemOption(models.Model):
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name='item_options')
    option_name = models.CharField(max_length=100)
    price_delta = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Option {self.option_name} for OrderItem {self.order_item.id}"
    
class OrderPromo(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    promo_code = models.ForeignKey(PromoCode, on_delete=models.CASCADE)
    applied_amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('order', 'promo_code')

