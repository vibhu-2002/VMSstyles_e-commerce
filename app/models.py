from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

STATE_CHOICES = (
    ('ENG', 'England'),
    ('SCT', 'Scotland'),
    ('WLS', 'Wales'),
    ('NIR', 'Northern Ireland'),
)
CATEGORY_CHOICES = (
    ('M', 'Mobile'),
    ('L', 'Laptop'),
    ('TW', 'Top Wear'),
    ('BW', 'Bottom Wear'),
)

class customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    locality = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50, choices=STATE_CHOICES)
    zipcode = models.IntegerField()

    def __str__(self):
        return str(self.id)
    class product(models.Model):
        title = models.CharField(max_length=100)
        selling_price = models.FloatField()
        discounted_price = models.FloatField()
        description = models.TextField()
        brand = models.CharField(max_length=100)
        category = models.CharField(max_length=2, choices=CATEGORY_CHOICES)

        product_image = models.ImageField(upload_to='productimg')
        def __str__(self):
            return str(self.id)
        
class cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    def __str__(self):
        return str(self.id)
    
STATE_CHOICES = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancelled', 'Cancelled'),
)
class orderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(customer, on_delete=models.CASCADE)
    product = models.ForeignKey('product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATE_CHOICES, default='Pending')
    


