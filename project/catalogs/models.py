from django.db import models

# In catalogs you should have: Restaurant — a restaurant that sells items. One restaurant has many menu items. MenuItem — a dish belonging to a single restaurant. Has a base price and availability. Category — groups like “Pizza”, “Drinks” ItemCategory (through-table) — many-to-many between MenuItem and Category, with an extra position field to control item ordering inside a category. Option — selectable add-on or variant (e.g., “Large”, “Extra cheese”). ItemOption (through-table) — many-to-many between MenuItem and Option, with extra fields such as price_delta (price adjustment for the option) and is_default (whether it’s preselected).
class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Option(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
class MenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menu_items')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    categories = models.ManyToManyField(Category, through='ItemCategory', related_name='menu_items')
    options = models.ManyToManyField(Option, through='ItemOption', related_name='menu_items')

    def __str__(self):
        return self.name
    
class ItemCategory(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    position = models.PositiveIntegerField()

    class Meta:
        unique_together = ('menu_item', 'category')

class ItemOption(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    price_delta = models.DecimalField(max_digits=10, decimal_places=2)
    is_default = models.BooleanField(default=False)

    class Meta:
        unique_together = ('menu_item', 'option')

    def __str__(self):
        return f"{self.option.name} for {self.menu_item.name}"
