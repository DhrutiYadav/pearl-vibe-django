from django.db import models
class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self): return self.name

class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    def __str__(self): return self.name

class Product(models.Model):
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    price = models.FloatField()
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    digital = models.BooleanField(default=False)

    # ✅ ADD THESE TWO LINES
    colors = models.JSONField(default=list, blank=True)   # multiple colors
    default_color = models.CharField(max_length=20, default="#8B4513")

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            return self.image.url
        except:
            return ''
